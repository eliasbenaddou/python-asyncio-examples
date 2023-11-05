import asyncio
import time


async def foo():
    print("foo")
    await asyncio.sleep(1)
    print("foo sleep")


async def bar():
    print("bar")
    time.sleep(0.3)
    await asyncio.sleep(0.5)
    print("bar sleep")


async def main():
    await asyncio.gather(foo(), bar())


asyncio.run(main())
