import asyncio



class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))

    def data_received(self, data):
        message = data.decode()
        handler = ClientServerProtocol.process(message)
        handler.add_metric()
        print('Data received: {!r}'.format(message))

        print('Following instance created with keys: {!r}'.format(handler.__dict__))
        self.transport.write(handler.get_dict())

        print('Close the client socket')
        self.transport.close()

    @staticmethod
    def process(message):
        args = message.split()
        return MetricHandler(*args)


class MetricHandler:

    metric_dict = {}

    def __init__(self, method, key=None, value=None, timestamp=None):
        self.method = method
        self.key = key
        self.value = value
        self.timestamp = timestamp

    def add_metric(self):
        MetricHandler.metric_dict[self.key] = self.value

    def get_dict(self):
        response = str(MetricHandler.metric_dict)
        return response.encode()



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