# Original https://github.com/KeepSafe/aiohttp

from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=text.encode('utf-8'))

async def wshandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.tp == web.MsgType.text:
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.tp == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.tp == web.MsgType.close:
            break

    return ws

async def octocat(request):
    with open("octocat.png", "rb") as f:
        return web.Response(body=f.read())
    return web.Response(body="Error loading image".encode('utf-8'))


app = web.Application()
app.router.add_route('GET', '/octocat', octocat)
app.router.add_route('GET', '/echo', wshandler)
app.router.add_route('GET', '/{name}', handle)
app.router.add_route('HEAD', '/{name}', handle)


web.run_app(app)
