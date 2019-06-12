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
            self.action(server_action)

    def action(self, server_action):
        if server_action == 'put':
            MetricHandler.add_metric()
            self.transport.write(b"OK\n\n")
        elif server_action == 'get':
            metric = MetricHandler.get_metric()
            response = "ok\n{}\n\n".format(metric).encode()
            self.transport.write(response)

    @staticmethod
    def create_handler(message):
        args = message.split()
        return MetricHandler(*args)

class MetricHandler:

    metric_dict = {}
    multi_vals = {}

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


    def add_metric(self):
        if self.metric_not_found:
            self.metric_dict[self.key] = [(self.value, self.timestamp)]
            self.multi_vals[self.key] = 0
        else:
            self.metric_update()

    def metric_update(self):
        value_list = self.metric_dict[self.key]
        new_value = value_list + [(self.value, self.timestamp)]
        self.metric_dict[self.key] = new_value
        self.multi_vals[self.key] += 1

    def get_metric(self):
        try:
            if self.key == '*':
                data = MetricParser.parse_all()
            elif multi_vals[self.key] > 0:
                data = MetricParser.parse_multi_value(self.key, multi_vals[self.key])
            else:
                data = MetricParser.parse_single_value(self.key)
        except KeyError:
            raise CommandError

class MetricParser:

    def __init__(self):
        self.dictionary = MetricHandler.metric_dict
        self.keys = self.dictionary.keys()
        self.values = self.dictionary.values()
        self.items = self.dictionary.items()

    def __repr__(self):
        pass

    def parse_all(self):
        all_keys_list = ['%s %s \n' % (key, value) for (key, value) in self.items]
        for element in all_keys_list:
            element = self.delete_brackets(element)
        return all_keys_list

    def parse_multi_value(self, key, count):
        values = self.delete_brackets(str(self.dictionary[key]))



    def parse_single_value(self, key):
        pass

    @staticmethod
    def delete_brackets(str):
        return re.sub('\[|\]|\(|\)', '', str)

    @staticmethod
    def sort_by_timestamp(values):
        pass


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
