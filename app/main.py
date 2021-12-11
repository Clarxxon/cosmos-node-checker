import asyncio
import aiohttp
from aiohttp import web
import aiojobs
import os

import logging

logger = logging.getLogger("core")
logger.setLevel(logging.INFO)

coins = [
    {
        "name": "juno-network",
        "validator_info_url": f"https://juno.api.ping.pub/staking/validators/{os.environ.get('VALIDATORS')}",
        "price_url": "https://api.coingecko.com/api/v3/simple/price?ids=juno-network&vs_currencies=usd",
    }
]


async def job(app, message="stuff", n=1):
    print("Asynchronous invocation (%s) of I'm working on")
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(verify_ssl=False)
    ) as session:
        for i in coins:
            usd_volume = 0
            async with session.get(i["validator_info_url"]) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    coin_volume = int(res["result"]["tokens"]) / 1000000
            async with session.get(i["price_url"]) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    coin_price = int(res[i["name"]]["usd"])
            usd_volume = coin_volume * coin_price
            print(usd_volume)

    await asyncio.sleep(30)
    await app["scheduled_job"].spawn(job(app))


async def handle(request):
    name = request.match_info.get("name", "Anonymous")
    text = f'Hello {name}, active jobs: {request.app["scheduled_job"].active_count}'
    return web.Response(text=text)


async def start_background_tasks(app):
    app["scheduled_job"] = await aiojobs.create_scheduler()
    await app["scheduled_job"].spawn(job(app=app))


async def cleanup_background_tasks(app):
    pass


app = web.Application()
app.add_routes([web.get("/", handle), web.get("/{name}", handle)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)


def init_func(argv):
    """python -m aiohttp.web -H localhost -P 8000 main:init_func"""
    logger.info("INFO: Запуск сервера.")
    logger.info("===" * 12)
    return app
