import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils import findProductPosition


logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class WaitingForSearchState(StatesGroup):
    waiting_for_query = State()
    waiting_for_id = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        '🧑🏻‍💻 Доброго времени суток!\nЯ являюсь практическим тестовым заданием\n'
        'для должности Python Developer 🐍 в ИП Ельмеев Данил Георгиевич\n'
        '\n<b>Введите поисковой запрос 🔡</b>\n<i>Например, Платье</i>',
        parse_mode='HTML'
    )
    await WaitingForSearchState.waiting_for_query.set()


@dp.message_handler(state=WaitingForSearchState.waiting_for_query)
async def process_query(message: types.Message, state: FSMContext):
    await state.update_data(query=message.text)
    await bot.send_message(
        message.from_user.id,
        'Отлично ✅\n'
        '<b>Введите артикул товара 🔢</b>\n'
        '<i>Например, 87989388</i>',
        parse_mode='HTML'
    )
    await WaitingForSearchState.waiting_for_id.set()


@dp.message_handler(state=WaitingForSearchState.waiting_for_id)
async def process_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    get_state = await state.get_data()
    id = get_state.get('id')
    query = get_state.get('query')

    await bot.send_message(
        message.from_user.id,
        'Произвожу поиск товара 🔃\nОжидайте 🚷',
        parse_mode='HTML'
    )

    results = await findProductPosition(id, query)

    if results['found'] == True:
        data = results['data']
        await bot.send_message(
            message.from_user.id,
            f'🟢 Товар найден\n<b>Страница: {data["page"]}\nНомер позиции: {data["position"]}</b>',
            parse_mode='HTML'
        )
    else:
        await bot.send_message(
            message.from_user.id,
            '🔴 К сожалению, товар не найден в выдаче запросов\n'
            'Возможно, вы ввели некорректные данные, либо ваш товар не попал в поисковую выдачу 😢',
            parse_mode='HTML'
        )

    await state.finish()


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.exception("Error in the bot")
