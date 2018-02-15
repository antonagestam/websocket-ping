import asyncio
from datetime import datetime
import uvloop
import sanic
from sanic.response import file

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = sanic.Sanic(__name__)
loop = asyncio.get_event_loop()


@app.route('/')
async def index(request):
    return await file('ws-test.html')


async def receive_ping(ws):
    """Wait for pings coming back and print the timediff"""
    while True:
        data = await ws.recv()
        dt = 1000 * (datetime.utcnow().timestamp() - float(data))
        print(f'ping: {dt}ms')


async def send_ping(ws):
    """Send pings to the web browser"""
    while True:
        await ws.send(f'{datetime.utcnow().timestamp()}')
        await asyncio.sleep(1)


@app.websocket('/join')
async def join(request, ws):
    await asyncio.gather(receive_ping(ws), send_ping(ws))


if __name__ == '__main__':
    try:
        import sys
        port = sys.argv[1]
    except IndexError:
        port = 8000
    app.run(host="0.0.0.0", port=port, debug=True)
