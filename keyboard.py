from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

menu_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Клавиатура', callback_data='keyboard')
        ],
        [
            InlineKeyboardButton(text='Машинное состояние', callback_data='FSM')
        ],
        [
            InlineKeyboardButton(text='Платежная система', callback_data='pay')
        ],
        [
            InlineKeyboardButton(text='API', callback_data='API')
        ],
        [
            InlineKeyboardButton(text='СУБД', callback_data='database')
        ],
        [
            InlineKeyboardButton(text='Медиа группы', callback_data='media')
        ]
    ]
)

menu_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Меню', callback_data='main')
        ]
    ]
)

menu_gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мужской'),
            KeyboardButton(text='Женский')
        ]
    ],
    resize_keyboard=True
    #one_time_keyboard=True
)
menu_basic = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
        ]
    ],
    resize_keyboard=True
    #one_time_keyboard=True
)