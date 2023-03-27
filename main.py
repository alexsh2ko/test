from aiogram import Bot, Dispatcher, types
import logging
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import csv
import webbrowser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import re


logging.basicConfig(level=logging.INFO)

API_TOKEN = '6286601698:AAFyd7gUZ2uGTK3GM3QESYXn5rg3At388uw'
ADMIN_CHAT_ID = '1016729616'
CSV_FILE = 'user_data.csv'

# Enter your website URL here
WEBSITE_URL = 'https://www.ukraine.uwc.org'

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)


class FAQ(StatesGroup):
    waiting_for_question = State()

class Registration(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_dob = State()
    waiting_for_email = State()
    waiting_for_phone = State()


FAQ_FILE = r"C:\Users\user\Desktop\test_bot\faq.csv"
def read_faq():
    with open(FAQ_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        faq = {}
        for row in reader:
            faq[row[0]] = row[1]
        return faq

def write_faq(faq):
    with open(FAQ_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for q, a in faq.items():
            writer.writerow([q, a])

@dp.message_handler(commands=['start', 'menu'])
async def welcome(message: types.Message):
    """
    This handler will be called when user sends /start command or taps on the Start button
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    faq_button = KeyboardButton('FAQ')
    register_button = KeyboardButton('Реєстрація')
    website_button = KeyboardButton('Відвідати веб-сайт')
    keyboard.add(faq_button, register_button, website_button)

    # Create the inline keyboard with the Start button
    start_button = InlineKeyboardButton('Start', callback_data='start')
    inline_keyboard = InlineKeyboardMarkup().add(start_button)

    # Send the welcome message with both keyboards
    await message.answer(f"Вітаємо у UWC Ukraine (United World Colleges) – "
                         f"це глобальна освітня програма, що робить освіту силою,"
                         f" яка об’єднує людей, нації та культури заради всесвітнього"
                         f" миру та стабільного майбутнього.\n\nЧим я можу допомогти?", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'start')
async def process_start_command(callback_query: types.CallbackQuery):
    await welcome(callback_query.message)
    await callback_query.answer()


@dp.message_handler(Text(equals='Visit Website'))
async def visit_website(message: types.Message):
    """
    This handler will be called when user taps on the Visit Website button
    """
    await message.answer(f"Opening {WEBSITE_URL}")
    # Open website using the user's default web browser
    webbrowser.open(WEBSITE_URL, new=2)

name_pattern = r'^[a-zA-Zа-яА-Я]+(([\'\,\.\- ][a-zA-Zа-яА-Я ])?[a-zA-Zа-яА-Я]*)*$'
dob_pattern = r'^\d{2}/\d{2}/\d{4}$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = re.compile(r'^\+\d{12}$')  # 12 digits after '+'

registration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ім'я"),
            KeyboardButton("Прізвище")
        ],
        [
            KeyboardButton("Дата народження")
        ],
        [
            KeyboardButton("Email адреса")
        ],
        [
            KeyboardButton("Номер телефона")
        ]
    ],
    resize_keyboard=True
)

# Handle the registration button
@dp.message_handler(Text(equals='Реєстрація'))
async def register(message: types.Message):
    # Ask for the user's first name
    await message.answer("Будь ласка введіть ваше ім'я:")
    await Registration.waiting_for_first_name.set()

# Handle the user's first name
@dp.message_handler(state=Registration.waiting_for_first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Validate the user's first name
        if not re.match(name_pattern, message.text):
            await message.answer("Невірне введення. Будь ласка введіть коректно ваше ім'я:")
            return

        data['first_name'] = message.text

        # Ask for the user's last name
        await message.answer("Будь ласка введіть ваше прізвище:")
        await Registration.waiting_for_last_name.set()

# Handle the user's last name
@dp.message_handler(state=Registration.waiting_for_last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Validate the user's last name
        if not re.match(name_pattern, message.text):
            await message.answer("Невірне введення. Будь ласка введіть коректно ваше прізвище:")
            return

        data['last_name'] = message.text

        # Ask for the user's date of birth
        await message.answer("Будь ласка, введіть дату вашого народження (ДД/ММ/РР):")
        await Registration.waiting_for_dob.set()

# Handle the user's date of birth
@dp.message_handler(state=Registration.waiting_for_dob)
async def process_dob(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Validate the user's date of birth
        if not re.match(dob_pattern, message.text):
            await message.answer("Невірне введення. Будь ласка введіть коректно дату вашого народження (ДД/ММ/РР):")
            return

        data['dob'] = message.text

        # Ask for the user's email address
        await message.answer("Будь ласка, введіть вашу email адресу:")
        await Registration.waiting_for_email.set()

# Handle the user's email address
@dp.message_handler(state=Registration.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Validate the user's email address
        if not re.match(email_pattern, message.text):
            await message.answer("Невірне введення. Будь ласка введіть коректно email адресу:")
            return

        data['email'] = message.text

        # Ask for the user's phone number
        await message.answer("Будь ласка, введіть номер вашого телефона (+XXXXXXXXXXXX):")
        await Registration.waiting_for_phone.set()

    # Handle the user's phone number
    @dp.message_handler(state=Registration.waiting_for_phone)
    async def process_phone(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            # Validate the user's phone number
            if not phone_pattern.match(message.text):
                await message.answer("Будь ласка, введіть коректно номер вашого телефона у форматі +XXXXXXXXXXXX.")
                return
            data['phone'] = message.text

            # Save the user's data to the CSV file
            with open(CSV_FILE, 'a', newline='') as f:
                fieldnames = ['First Name', 'Last Name', 'Date of Birth', 'Email Address', 'Phone Number']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # Write headers if file is empty
                if f.tell() == 0:
                    writer.writeheader()

                # Write data
                writer.writerow({
                    'First Name': data['first_name'],
                    'Last Name': data['last_name'],
                    'Date of Birth': data['dob'],
                    'Email Address': data['email'],
                    'Phone Number': data['phone']
                })

            # End the conversation
            await message.answer("Дякуємо за реєстрацію!")
            await state.finish()





@dp.message_handler(lambda message: message.text == 'FAQ')
async def faq_message(message: types.Message):
    faq = read_faq()
    keyboard = types.InlineKeyboardMarkup()
    for q in faq.keys():
        keyboard.add(types.InlineKeyboardButton(q, callback_data=q))
    await message.answer('Here are some frequently asked questions:', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in read_faq().keys())
async def faq_callback(callback_query: types.CallbackQuery):
    faq = read_faq()
    answer = faq[callback_query.data]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, answer)


@dp.message_handler(lambda message: message.text == 'FAQ')
async def faq_message(message: types.Message):
    faq = read_faq()
    keyboard = types.InlineKeyboardMarkup()
    for q in faq.keys():
        keyboard.add(types.InlineKeyboardButton(q, callback_data=q))
    await message.answer('Here are some frequently asked questions:', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in read_faq().keys())
async def faq_callback(callback_query: types.CallbackQuery):
    faq = read_faq()
    answer = faq[callback_query.data]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, answer)
if __name__ == '__main__':
    asyncio.run(executor.start_polling(dp, skip_updates=True))