"""Gate 2 check: 10 complaints, and an AI that needs 1 second for each one.

python -m scripts.async_demo sync    one by one
python -m scripts.async_demo trap    async def, but with a blocking call inside
python -m scripts.async_demo async   truly async
"""
import asyncio
import sys
import time

import httpx

URL = "http://localhost:9000/classify"
HEADERS = {"Authorization": "Bearer lab-secret-123"}
BODY = {"complaint": "I was charged twice for my biryani"}
N = 10


def one_by_one() -> None:
    with httpx.Client(timeout=10) as client:
        for _ in range(N):
            client.post(URL, json=BODY, headers=HEADERS)


async def blocking_inside_async() -> None:
    async def ask() -> None:
        httpx.post(URL, json=BODY, headers=HEADERS, timeout=10)   # the trap: this call blocks
    await asyncio.gather(*(ask() for _ in range(N)))


async def truly_async() -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        await asyncio.gather(*(client.post(URL, json=BODY, headers=HEADERS) for _ in range(N)))


mode = sys.argv[1] if len(sys.argv) > 1 else "async"
start = time.perf_counter()
if mode == "sync":
    one_by_one()
elif mode == "trap":
    asyncio.run(blocking_inside_async())
else:
    asyncio.run(truly_async())
print(f"{mode:5}: {N} complaints in {time.perf_counter() - start:.1f} seconds")
