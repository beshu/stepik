import asyncio

async def handle_echo(message, loop):

    reader, writer = await asyncio.open_connection('127.0.0.1', 8181, loop=loop)
    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

message = 'put eardrum.cpu 10.6 1501864247'
loop = asyncio.get_event_loop()
loop.run_until_complete(handle_echo(message, loop))
loop.close()
