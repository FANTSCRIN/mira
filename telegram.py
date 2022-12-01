from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from configs.config_tokens import token_telegram
from configs.config_mira import buttons
from aiogram.utils.markdown import code
from sql import Database
from mira import Mira
import asyncio
import random

mira = Mira()          # Мира
db = Database()        # База данных
name_app = 'TELEGRAM'  # Название приложения

bot = Bot(token=token_telegram)
dp = Dispatcher(bot)


# Авторизация бота
def auth() -> None:
    global bot
    global dp
    bot = Bot(token=token_telegram)
    dp = Dispatcher(bot)


# Формирование клавиатуры
def get_keyboard(names_buttons: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for row in names_buttons:
        for but in row:
            button = KeyboardButton(buttons[but])
            markup.insert(button)
        markup.row()

    return markup


@dp.message_handler()
async def echo(message: types.Message):
    # data = mira.select_command(from_where=name_app, from_id=message.from_user.id, text_message=message.text.strip())
    markup = get_keyboard([['команды', 'генераторы'], ['назад']])
    await message.answer('Новая клава', reply_markup=markup)

# Запуск приложения
if __name__ == '__main__':
    try:
        # mira.output_name_app_start(name_app, 'start')
        # executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=start_tasks)
        executor.start_polling(dispatcher=dp, skip_updates=True)
    except Exception as message:
        # MIRA.output_name_app_start(NAME_APP, 'restart!' + str(message))
        auth()
