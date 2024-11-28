from aiogram import types, Dispatcher, executor, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
but1 = KeyboardButton(text="Рассчитать")
but2 = KeyboardButton(text="Информация")
kb.add(but1, but2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = int(int(data["weight"]) * 10 + 6.25 * int(data["growth"]) - 4.92 * int(data["age"]))
    await message.answer(f"Ваша норма калорий в день составляет: {res}")
    await state.finish()


@dp.message_handler(commands=["start"])
async def com_start(message):
    await message.answer("lfhjdf" ,reply_markup=kb)


@dp.message_handler(text="Информация")
async def information(message):
    await message.answer("Информация про бота!")


@dp.message_handler()
async def all_message(message):
    await message.answer("asd")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
