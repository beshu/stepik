import asyncio
import re

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
            if server_action == 'put':
                metric_handler.add_metric()
                self.transport.write(b"OK\n\n")
            elif server_action == 'get':
                metric = metric_handler.get_metric()
                response = "ok\n{}\n\n".format(metric).encode()
                self.transport.write(response)

        #print('All entries: {!r}'.format(metric_handler.__dict__))

    @staticmethod
    def create_handler(message):
        args = message.split()
        return MetricHandler(*args)

class MetricHandler:

    metric_dict = {}

    def __init__(self, method, key=None, value=None, timestamp=None):
        if method not in ('put','get'):
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

    def add_metric(self):
        if self.metric_not_found:
            self.metric_dict[self.key] = [(self.value, self.timestamp)]
        else:
            self.metric_update()

    def metric_update(self):
        value_list = self.metric_dict[self.key]
        new_value = value_list + [(self.value, self.timestamp)]
        self.metric_dict[self.key] = new_value

    def get_metric(self):
        response_dict = {}
        try:
            if self.key == '*':
                response_dict.update(self.metric_dict)
            else:
                response_dict.update({self.key:self.metric_dict[self.key]})
            data = str(response_dict)
            return data.encode()
        except KeyError:
            return str(dict()).encode()

    def get_dict(self):
        data = str(self.metric_dict)
        return data.encode()


class DictParser:

    def __init__(self, dictionary, action):
        self.dictionary = dictionary
        self.action = action

    def __repr__(self):
        pass


    def parse_all(self):
        all_metrics = self.dictionary.items()
        strings_list = ['%s %s \n' % (key, value) for (key, value) in all_metrics]
        for element in strings_list:
            element = self.delete_brackets(element)
        return strings_list

    def parse_multi_value(self):
        values = self.dictionary.values()


    def parse_single_value(self):
        pass

    @staticmethod
    def delete_brackets(str):
        return re.sub('\[|\]|\(|\)', '', str)

class CommandError(Exception):
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
