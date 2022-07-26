async def abc():
    print('a')
    await sleep(3)
    print('b')
    await sleep(3)
    print('c')

async def sleep(n):
    time.sleep(n)

import asyncio, time


loop = asyncio.get_event_loop()
loop.run_until_complete(abc())