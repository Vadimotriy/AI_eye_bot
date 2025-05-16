import asyncio
import concurrent.futures
from aiogram import types

from bot.bot import AI, bot


class AsyncQueue:
    # инициализация
    def __init__(self):
        self.queue = asyncio.Queue()
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.is_processing = False

    # добавление в очередь
    async def add_task(self, user_id, image_bytes, langs):
        await self.queue.put((user_id, image_bytes, langs))
        if not self.is_processing:
            asyncio.create_task(self.process_queue())

    # обработка
    async def process_queue(self):
        self.is_processing = True
        while not self.queue.empty():
            user_id, image_bytes, langs = await self.queue.get()
            try:
                # запуск easyocr в отдельном потоке
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    AI.get_text,
                    image_bytes,
                    langs
                )
                await self.send_result(user_id, result)
            except Exception as e:
                await self.send_error(user_id, str(e))
            finally:
                self.queue.task_done()
        self.is_processing = False

    # отправка результата
    async def send_result(self, user_id, result):
        if result[0][0]:
            text = "\n".join(result[0])
            image = result[1]
            if len(text) > 1000:
                await bot.send_photo(
                    chat_id=user_id, caption=f"Изображение",
                    photo=types.BufferedInputFile(file=image.getvalue(), filename="image.png")
                )
                await bot.send_message(chat_id=user_id, text=f"Результат:\n\n{text}", parse_mode=None)
            else:
                await bot.send_photo(
                    chat_id=user_id, caption=f"Результат:\n\n{text}",
                    photo=types.BufferedInputFile(file=image.getvalue(), filename="image.png"),
                    parse_mode=None
                )
        else:
            await bot.send_message(chat_id=user_id, text=f"Текст не найден.")

    # для отладки
    async def send_error(self, user_id, error):
        await bot.send_message(chat_id=user_id, text=f"Ошибка! Вероятнее всего, у вас несовместимые язки.")
