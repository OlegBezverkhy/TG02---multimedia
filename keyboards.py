from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Привет'), KeyboardButton(text = 'Пока')]], resize_keyboard=True)

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Видео', url='https://dzen.ru/video/watch/66af567757e7bc5b7b2a5fc5?share_to=link')],
    [InlineKeyboardButton(text='Песня', url='https://my.mail.ru/music/songs/72130843328d8a3c7a93262f956aba52')],
    [InlineKeyboardButton(text='Новости', url='https://www.sobaka.com/pro-sobak/sobachi-novosti/?ysclid=m27wo0uymv79729469')]
])


inline_keyboard_more = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Показать больше...', callback_data='more')]])

key_list = ['Опция 1','Опция 2','Опция 3','Опция 4']

async def option_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in key_list:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=f'option:{key}'))
    return keyboard.adjust(1).as_markup()