# https://community.nitrous.io/tutorials/asynchronous-programming-with-python-3

import aiohttp
import asyncio
import itertools

async def download(url, parts=16):

    print("URL: {}".format(url))

    async def get_partial_content(_url, _part, start, end):

        print("Part {}/{} (Bytes {} to {})".format(_part, parts, start, end))

        h = {"Range": "bytes={}-{}".format(start, end - 1 if end else "")}
        async with aiohttp.get(_url, headers=h) as resp:
            return _part, await resp.read()

    async with aiohttp.head(url) as resp:
        size = int(resp.headers["Content-Length"])

    ranges = list(range(0, size, size // parts))
    res, _ = await asyncio.wait(
        [get_partial_content(url, i, start, end) for i, (start, end) in
         enumerate(itertools.zip_longest(ranges, ranges[1:], fillvalue=""))])
    sorted_result = sorted(task.result() for task in res)

    return b"".join(data for _, data in sorted_result)


if __name__ == '__main__':

    url = "http://github-images.s3.amazonaws.com/blog/2011/cc-wallpaper-desktop.png"
    loop = asyncio.get_event_loop()
    bs = loop.run_until_complete(download(url))

    with open("test_async.png", "wb") as f:
        f.write(bs)
