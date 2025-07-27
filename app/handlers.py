from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generators import gpt

router = Router()

class Generate(StatesGroup):
    text = State()


@router.message(CommandStart())
async def cmd_start(message:Message, state:FSMContext):
    await state.clear()
    await message.answer(text='Добро пожаловать в бот')


@router.message(F.text)
async def generate(message:Message, state:FSMContext):
    await state.set_state(Generate.text)
    await message.answer(gpt(message.text))
    await state.clear()


@router.message(Generate.text)
async def generate_error(message:Message):
    await message.answer("Погоди! Не торопись пись пись...")