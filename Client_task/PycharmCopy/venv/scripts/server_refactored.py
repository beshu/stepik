import asyncio
import re
import itertools

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))

    def data_received(self, data):
        message = data.decode()
        try:
            metric_handler = self.create_handler(message)
        except CommandError:
            self.transport.write(b"error\nwrong command\n\n")
        else:
            server_action = metric_handler.method
            self.action(server_action, metric_handler)

    def action(self, server_action, handler):
        if server_action == 'put':
            handler.add_metric()
            self.transport.write(b"OK\n\n")
        elif server_action == 'get':
            metric_list = handler.get_metric()
            response = "ok\n{}\n\n".format(metric_list).encode()
            self.transport.write(response)

    @staticmethod
    def create_handler(message):
        args = message.split()
        return Metric(*args)

    @staticmethod
    def multi_val(data_list):
        if len(data_list) > 3:
            return True


class Metric:

    metric_dict = {}

    def __init__(self, method, key=None, value=None, timestamp=None):
        if method not in ('put', 'get'):
            raise CommandError
        else:
            self.method = method
        self.key = key
        self.value = value
        self.timestamp = timestamp

    @property
    def metric_not_found(self):
        if self.key not in self.metric_dict.keys():
            return True

    @property
    def multi_val(self):
        if len(self.get_values_global(self.key)) > 1:
            return True

    def get_values_global(self, key):
        return self.metric_dict[key]

    def add_metric(self):
        if self.metric_not_found:
            self.metric_dict[self.key] = [(self.value, self.timestamp)]
        else:
            self.metric_update()

    def metric_update(self):
        value_list = self.metric_dict[self.key]
        new_value = value_list + [(self.value, self.timestamp)]
        self.metric_dict[self.key] = self.sorted_by_timestamp(new_value)

    def get_metric(self):
        response_dict = {}
        try:
            if self.key == '*':
                response_dict.update(self.metric_dict)
                data_list = self.parse_all(response_dict)
            else:
                response_dict.update({self.key: self.get_values_global(self.key)})
                if self.multi_val:
                    data_list = self.parse_multi(response_dict, self.key)
                else:
                    data_list = self.parse_single(response_dict, self.key)
            return data_list
        except KeyError:
            raise CommandError

    def parse_all(self, dct):
        pass

    def parse_multi(self, dct, key):
        strings_list = []
        count = range(len(dct[key]))
        values = dct[key]
        i = 0
        input_str = ''
        for _ in count:
            value = self.delete_brackets(str(values[i]))
            formatted = '{}{}'.format(key, value)
            input_str.join(formatted)
            strings_list.append(input_str)
            i += 1
        return strings_list

    def parse_single(self, dct, key):
        pass

    @staticmethod
    def sorted_by_timestamp(value_list):
        sorted_list = sorted(value_list, key = lambda timestamp: timestamp[1])
        return sorted_list

    @staticmethod
    def delete_brackets(str):
        return re.sub('\[|\]|\(|\)', '', str)


class CommandError(BaseException):
    pass

loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8181
)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
