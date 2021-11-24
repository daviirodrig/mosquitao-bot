import aiohttp
import asyncio
import random

boards = ['a', 'c', 'w', 'm', 'cgl', 'cm', 'n', 'jp', 'vp', 'v', 'vg', 'vr', 'co', 'g', 'tv', 'k', 'o', 'an', 'tg', 'sp', 'asp', 'sci', 'int', 'out', 'toy', 'biz', 'i', 'po', 'p', 'ck', 'ic',
          'wg', 'mu', 'fa', '3', 'gd', 'diy', 'wsg', 's', 'hc', 'hm', 'h', 'e', 'u', 'd', 'y', 't', 'hr', 'gif', 'trv', 'fit', 'x', 'lit', 'adv', 'lgbt', 'mlp', 'b', 'r', 'r9k', 'pol', 'soc', 's4s']
cache = {cache: '' for cache in boards}


async def r4chan():
    board = random.choice(boards)
    threadnums = list()
    data = ''

    if (cache[board] != ''):
        data = cache[board]
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://a.4cdn.org/' + board + '/catalog.json') as r:
                data = await r.json()
        cache[board] = data
        await asyncio.sleep(1.1)

    for page in data:
        for thread in page["threads"]:
            threadnums.append(thread['no'])

    thread = random.choice(threadnums)

    # Request the thread information, and get a list of images in that thread; again sleeping for 1.5 seconds
    imgs = list()
    async with aiohttp.ClientSession() as session:
        async with session.get('http://a.4cdn.org/' + board + '/thread/' + str(thread) + '.json') as r:
            pd = await r.json()
    for post in pd['posts']:
        try:
            imgs.append(str(post['tim']) + str(post['ext']))
        except:
            pass
    await asyncio.sleep(1.1)

    image = random.choice(imgs)
    imageurl = 'https://i.4cdn.org/' + board + '/' + image
    thread = 'https://boards.4chan.org/' + board + '/thread/' + str(thread)
    return [imageurl, thread]


async def main():
    url = await r4chan()
    return url[0]
