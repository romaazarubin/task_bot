import requests
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery, MediaGroup, InputFile, LabeledPrice, PreCheckoutQuery
from main import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from requests import get
from config import pay_token
from aiogram.types.message import ContentType
from keyboard import menu_main, menu_back, menu_gender, menu_basic, menu_database
from sql import DateBase
from fsm_state import Bio
import random

price = [LabeledPrice(label='Наушники', amount=40000)]

db = DateBase("db.db")


@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Список заданий',
                           reply_markup=menu_main)


@dp.callback_query_handler(text_contains='keyboard')
async def task_one(call: CallbackQuery):
    await call.message.edit_text(text=call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=menu_back)


@dp.callback_query_handler(text_contains='main')
async def main(call: CallbackQuery):
    await call.message.edit_text(text='Список заданий')
    await call.message.edit_reply_markup(reply_markup=menu_main)


@dp.callback_query_handler(text_contains='FSM', state=None)
async def point1(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(text='Выберите пол', reply_markup=menu_gender)

    await Bio.step1.set()


@dp.message_handler(state=Bio.step1)
async def step1(message: Message, state: FSMContext):
    gender = message.text
    await state.update_data(
        {
            'gender': gender
        }
    )
    await bot.send_message(message.from_user.id, text="Пришлите фотографию", reply_markup=ReplyKeyboardRemove())
    await Bio.step2.set()


@dp.message_handler(content_types=['photo'], state=Bio.step2)
async def echo_photo_bot(message: Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('gender')
    await bot.send_photo(message.chat.id, message.photo[0].file_id, caption=f"Имя - {message.from_user.username}\n"
                                                                            f"Пол - {text}")

    await bot.send_message(message.chat.id, text='Вернуться на главное меню', reply_markup=menu_basic)
    await state.finish()


@dp.message_handler(Text(equals=["Меню"]))
async def menu(message: Message):
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id,
                           text='Список заданий',
                           reply_markup=menu_main)


@dp.callback_query_handler(text_contains='API')
async def task_four(call: CallbackQuery):
    usd_jsn = 'https://www.cbr-xml-daily.ru/daily_json.js'
    updates = requests.get(usd_jsn)
    text = updates.json()['Valute']['USD']['Value']
    await call.message.edit_text(text=f'Курс USD - {text}', reply_markup=menu_main)


@dp.callback_query_handler(text_contains='media')
async def task_six(call: CallbackQuery):
    media = MediaGroup()
    media.attach_photo(InputFile('media/196769.jpg'))
    media.attach_photo(InputFile('media/interer-bmw-m5-1536x864.jpg'))
    media.attach_photo(InputFile('media/bmw-m5-competition-f90-chetyriokhdvernyi-2018-seryi-4x4-seda.jpg'))
    await bot.send_media_group(call.message.chat.id, media=media)


@dp.callback_query_handler(text_contains='pay')
async def buy_cart(call: CallbackQuery):
    await bot.send_invoice(call.message.chat.id,
                           title='Cart',
                           description='Description',
                           provider_token=pay_token,
                           currency='rub',
                           need_phone_number=True,
                           is_flexible=False,
                           prices=price,
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def s_pay(message: Message):
    await bot.send_message(message.chat.id, f'Название товара - {price[0]["label"]} \n'
                                            f'Цена товара - {price[0]["amount"] // 100} рублей.',
                           reply_markup=menu_main)


@dp.callback_query_handler(text_contains='database')
async def menu(call: CallbackQuery):
    await call.message.edit_text(text='Список заданий',
                                 reply_markup=menu_database)


@dp.callback_query_handler(text_contains='add_user')
async def menu(call: CallbackQuery):
    num = random.randint(1, 100)
    try:
        await db.add_users(call.from_user.id, call.message.chat.first_name, call.from_user.username, num)
    except Exception as e:
        pass
    finally:
        await call.message.edit_text(text='Список заданий', reply_markup=menu_database)


@dp.callback_query_handler(text_contains='user_presence')
async def presence(call: CallbackQuery):
    try:
        k = await db.user_presence(call.from_user.id)
        if k == 0:
            await call.message.edit_text(text='Пользователь отсутвует', reply_markup=menu_database)
        else:
            await call.message.edit_text(text='Пользователь есть в базе', reply_markup=menu_database)
    except Exception as e:
        await call.message.edit_text(text='Ошибка', reply_markup=menu_database)


@dp.callback_query_handler(text_contains='change_name')
async def cnahge(call: CallbackQuery):
    try:
        await db.update_name(call.from_user.id)
        await call.message.edit_text(text='Имя изменено', reply_markup=menu_database)
    except Exception as e:
        await call.message.edit_text(text='Имя не изменено', reply_markup=menu_database)


@dp.callback_query_handler(text_contains='delete_user')
async def delet(call: CallbackQuery):
    try:
        await db.user_del(call.from_user.id)
        await call.message.edit_text(text='Пользователь удален', reply_markup=menu_database)
    except Exception as e:
        await call.message.edit_text(text='Пользователь не удален', reply_markup=menu_database)


@dp.callback_query_handler(text_contains='take_num')
async def delet(call: CallbackQuery):
    try:
        num = await db.take_num(call.from_user.id)
        await call.message.edit_text(text=f'{num}')
    except Exception as e:
        await call.message.edit_text(text='Ошибка')
