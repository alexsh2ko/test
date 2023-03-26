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

logging.basicConfig(level=logging.INFO)

API_TOKEN = '6286601698:AAFyd7gUZ2uGTK3GM3QESYXn5rg3At388uw'
ADMIN_CHAT_ID = '1016729616'
CSV_FILE = r'C:\Users\user\Desktop\test_bot\user_data.csv'

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
    waiting_for_name = State()
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
    register_button = KeyboardButton('Register')
    website_button = KeyboardButton('Visit Website')
    keyboard.add(faq_button, register_button, website_button)

    # Create the inline keyboard with the Start button
    start_button = InlineKeyboardButton('Start', callback_data='start')
    inline_keyboard = InlineKeyboardMarkup().add(start_button)

    # Send the welcome message with both keyboards
    await message.answer("Вітаємо у UWC Ukraine!\nWhat can I do for you?", reply_markup=keyboard)


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

registration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("First Name"),
            KeyboardButton("Last Name")
        ],
        [
            KeyboardButton("Date of Birth")
        ],
        [
            KeyboardButton("Email Address")
        ],
        [
            KeyboardButton("Phone Number")
        ]
    ],
    resize_keyboard=True
)

# Handle the registration button
@dp.message_handler(Text(equals='Register'))
async def register(message: types.Message):
    # Ask for the user's first and last name
    await message.answer("Please enter your first and last name:")
    await Registration.waiting_for_name.set()

# Handle the user's name
@dp.message_handler(state=Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data: 
        data['name'] = message.text

        # Ask for the user's date of birth
        await message.answer("Please enter your date of birth (DD/MM/YYYY):")
        await Registration.waiting_for_dob.set()

# Handle the user's date of birth
@dp.message_handler(state=Registration.waiting_for_dob)
async def process_dob(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dob'] = message.text

        # Ask for the user's email address
        await message.answer("Please enter your email address:")
        await Registration.waiting_for_email.set()

# Handle the user's email address
@dp.message_handler(state=Registration.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

        # Ask for the user's phone number
        await message.answer("Please enter your phone number:")
        await Registration.waiting_for_phone.set()

# Handle the user's phone number
@dp.message_handler(state=Registration.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

        # Save the user's data to the CSV file
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([data['name'], data['dob'], data['email'], data['phone']])

        # End the conversation
        await message.answer("Thank you for registering!")
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