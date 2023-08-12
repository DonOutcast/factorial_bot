from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from model.template.templates import render
from model.fsm.factorial import FactorialStates
from model.keyboards.core_buttons import generate_keyboard
from model.utils.validation import validate_number_of_factorial
from model.services.factorial import calculate_factorial_threaded, calculate_and_print_factorial

menu_keyboard = generate_keyboard(
    [
        [
            "Факториал 🧾",
        ],

    ],
)

back_to_menu = generate_keyboard(
    [
        [
            "Вернуться в главное меню 📜",
        ],
    ]
)

user_router = Router()
headers = {"throttling_key": "default", "long_operation": "typing"}


@user_router.message(CommandStart(), flags=headers)
async def user_start(message: Message):
    await message.answer(text=render.render_template(template_name="start.html"), reply_markup=menu_keyboard)


@user_router.message(F.text == "Факториал 🧾", flags=headers)
async def get_factorial(message: Message, state: FSMContext):
    await message.answer(text=render.render_template(template_name="factorial.html"), reply_markup=back_to_menu)
    await state.set_state(FactorialStates.number)


@user_router.message(F.content_type.in_("text"), FactorialStates.number, flags=headers)
async def get_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await state.clear()
    if validate_number_of_factorial(data.get("number")):
        await message.answer(text=f"{calculate_and_print_factorial(int(data.get('number')))}")
    else:
        await message.answer(
            text=render.render_template(template_name="factorial_error.html"),
            reply_markup=menu_keyboard
        )
