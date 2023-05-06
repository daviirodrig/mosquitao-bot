import asyncio
import random
import aiohttp
from cmds.helpers.consts import boards

cache = {cache: '' for cache in boards}


async def r4chan():
    board = random.choice(boards)
    threadnums = []
    data = ""

    if cache[board] != "":
        data = cache[board]
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://a.4cdn.org/" + board +
                                   "/catalog.json") as r:
                data = await r.json()
        cache[board] = data
        await asyncio.sleep(1.1)

    for page in data:
        for thread in page["threads"]:
            threadnums.append(thread["no"])

    thread = random.choice(threadnums)

    imgs = []
    async with aiohttp.ClientSession() as session:
        async with session.get("http://a.4cdn.org/" + board + "/thread/" +
                               str(thread) + ".json") as r:
            pd = await r.json()
    for post in pd["posts"]:
        try:
            imgs.append(str(post["tim"]) + str(post["ext"]))
        except:
            pass
    await asyncio.sleep(1.1)

    image = random.choice(imgs)
    imageurl = "https://i.4cdn.org/" + board + "/" + image
    thread = "https://boards.4chan.org/" + board + "/thread/" + str(thread)
    return [imageurl, thread]


async def main():
    url = await r4chan()
    return url


if __name__ in "__main__":
    posts = asyncio.run(main())
    print(f"Image: {posts[0]}")
    print(f"Thread: {posts[1]}")
    print("--------------------------------------------------")
