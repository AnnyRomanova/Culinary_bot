import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from aiogram import Dispatcher, Bot, types

from src.culinary import Culinary


# Настраиваем конфигурацию для бота
# Подтягиваем данные из виртуального окружения
class BotConfig(BaseSettings):
    token: str

    class Config:
        env_file = ".env"
        env_prefix = "BOT_"


class CulinaryBot:
    def __init__(self, config: BotConfig):
        self.config = config
        self.culinary = Culinary()
        # создаем диспетчер для обработки запросов
        self.dp = Dispatcher()
        # объект бота из библиотеки aiogram, передается в методы диспетчера
        self.bot = Bot(config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.register_handlers()

    # метод регистрирует методы работы с ботом
    def register_handlers(self):
        self.dp.message.register(self.start_handler, CommandStart())
        self.dp.message.register(self.text_message_handler)  # Обработчик текстовых сообщений

    # Создание inline-клавиатуры с кнопками-ссылками
    async def get_inline_keyboard(self, message: types.Message):
        recipe_dict = await self.culinary.get_recipe(message.text)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for title, link in recipe_dict.items():
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=title, url=link)])

        return keyboard

    # Обработчик текстовых сообщений
    async def text_message_handler(self, message: types.Message):
        # получаем inline-клавиатуру
        keyboard = await self.get_inline_keyboard(message)
        await message.answer("Вот несколько подходящих рецептов:", reply_markup=keyboard)

    # Приветствие
    async def start_handler(self, message: types.Message):
        await message.answer("Привет! Напиши блюдо, которое хотелось бы приготовить.")

    # Запуск бота через метод библиотеки aiogram - start_polling
    async def start(self):
        await self.dp.start_polling(self.bot)


async def main():
    load_dotenv()
    config = BotConfig()
    bot = CulinaryBot(config)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())