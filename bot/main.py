import asyncio

from bot import bot, dp
# from handlers.handlers import router, router_callbacks

if __name__ == '__main__':  # запуск программы
    # dp.include_router(router)
    # dp.include_router(router_callbacks)


    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


    asyncio.run(main())