import logging
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command

# Set up logging
logging.basicConfig(level=logging.INFO)
TOKEN_API = '6286601698:AAFyd7gUZ2uGTK3GM3QESYXn5rg3At388uw'
# Initialize bot and dispatcher
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

# Initialize Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Set up Google Sheets database
sheet = client.open('UWC Ukraine User Database').sheet1

# Define welcome message
welcome_message = """
Welcome to UWC Ukraine Bot!
"""

# Define FAQ message
faq_message = """
Here are some frequently asked questions about UWC Ukraine:

Q: What is UWC Ukraine?
A: UWC Ukraine is a national committee of UWC that selects, prepares, and supports Ukrainian students for admission to UWC schools and colleges.

Q: How can I apply to UWC Ukraine?
A: Please visit our website at https://www.ukraine.uwc.org/apply to learn more about our application process.

Q: What are the eligibility requirements for UWC Ukraine?
A: We consider candidates who are Ukrainian citizens or have been residents of Ukraine for at least two years, and who are between the ages of 16 and 18 at the time of entry to a UWC school or college.

Q: What schools and colleges are part of UWC?
A: UWC has 18 schools and colleges around the world, including one in Dilijan, Armenia.

Q: How can I support UWC Ukraine?
A: We appreciate any and all support for our mission of making education a force for peace and sustainability. Please visit our website at https://www.ukraine.uwc.org/donate to learn more about how to donate or get involved.

If you have any other questions or concerns, please don't hesitate to contact us at uwc.ukraine@gmail.com.
"""

# Define user registration message and keyboard
registration_message = """
Please fill out the following form to register for UWC Ukraine:
"""

registration_keyboard = InlineKeyboardMarkup(row_width=1)
registration_button = InlineKeyboardButton('Register', url='https://docs.google.com/forms/d/e/1FAIpQLSfW4IvjrE-lZWWJz2kFb6W9z6aKp7Vh1dG8f7VbPvC7Z3qgGg/viewform')
registration_keyboard.add(registration_button)

# Define website button and keyboard
website_keyboard = InlineKeyboardMarkup(row_width=1)
website_button = InlineKeyboardButton('Visit our website', url='https://www.ukraine.uwc.org')
website_keyboard.add(website_button)

# Define push notification function
async def send_push_notification(user_id: int, message: str):
    try:
        await bot.send_message(chat_id=user_id, text=message)
        logging.info(f"Push notification sent to user {user_id}: {message}")
    except Exception as e:
        logging.error(f"Error sending push notification to user {user_id}: {str(e)}")

# Define handler for start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer
