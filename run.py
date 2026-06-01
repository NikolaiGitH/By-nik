
import os
import aiohttp
import aiohttp.resolver

# Принудительно используем ThreadedResolver вместо aiodns
aiohttp.resolver.DefaultResolver = aiohttp.resolver.ThreadedResolver

from aiohttp import web
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router

async def handle(request):
    return web.Response(text="Bot is live")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")
    return runner

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    runner = await start_web_server()
    
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
