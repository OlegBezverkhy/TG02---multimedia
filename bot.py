import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from deep_translator import GoogleTranslator
from gtts import gTTS
from secure import TG_TOKEN, OPEN_WEATHERMAP
from data import JOKES, TRAININGS
from random import choice
import os
import requests
import keyboards as kb


bot = Bot(token=TG_TOKEN)
dispatcher = Dispatcher()


def get_weather(city, city_ru):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHERMAP}&units=metric"
    response = requests.get(url, timeout=20)
    if response.status_code == 200:
        data = response.json()
        main = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_report = (
            f"Погода в городе {city_ru}:\n"
            f"Описание: {main}\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        return weather_report
    else:
        return "Не удалось получить данные о погоде."


def lang(text):
    first_char = text[0].lower()
    if 'a' <= first_char <= 'z':
        language = 'ru'
    elif 'а' <= first_char <= 'я':
        language = 'en'
    else:
        return None
    return language


def translate_text(text):
    target_language = lang(text)
    if not (target_language is None):
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
    else:
        translated = 'Я такого слова не знаю'
    return translated


@dispatcher.message(F.text == 'привет')
async def greeting(message: Message):
    await message.answer('Приятно встретить воспитанного человека. Не так часто боту говорят привет. '
                             'А мы так любим вежливых людей')


@dispatcher.message(F.photo )
async def ansewer_photo(message: Message):
    answer_list = ['Классное фото', 'Что это?', 'Не надо мне это показывать больше',
                   'Фотографу руки оторвать', 'Удачный кадр!']
    await message.answer(choice(answer_list))
    await bot.download(message.photo[-1], destination=f'tmp/photo/{message.photo[-1].file_id}.jpg')


@dispatcher.message(F.audio)
async def audio_message_save(message: Message):
    answer_list = ['Я все запомнил', 'Зачем мне эта информация?', 'Даже не говори!',
                   'Хорошо', 'Отличное известие']
    await message.answer(choice(answer_list))
    if message.audio is None:
        await message.answer("Это не аудиофайл.")
        return
    file_id = message.audio.file_id
    try:
        file = await bot.get_file(file_id)
        destination = f'tmp/voice_message/{file_id}.ogg'
        await bot.download_file(file.file_path, destination)
        await message.answer(f"Файл сохранен как {destination}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при загрузке файла: {str(e)}")




@dispatcher.message(F.text == 'Привет')
async def test_button1(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}!')


@dispatcher.message(F.text == 'Пока')
async def test_button1(message: Message):
    await message.answer(f'До свидания {message.from_user.first_name}!')


@dispatcher.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять комманды \n'
                         '/start - запуск \n'
                         '/help - помощь \n'
                         '/joke - шутка \n'
                         '/forecast - прогноз погоды \n'
                         '/photo - пришлет тебе фото')


@dispatcher.message(Command('joke'))
async def jokes(message: Message):
    await message.answer(choice(JOKES))


@dispatcher.message(Command('links'))
async def jokes(message: Message):
    await message.answer('Мои любимые ссылки :', reply_markup=kb.inline_keyboard)


@dispatcher.callback_query(F.data == 'more')
async def more(callback:CallbackQuery):
    await callback.answer('Выбор опций формируется', show_alert=True)
    await callback.message.edit_text('Вот Ваши опции:', reply_markup= await kb.option_keyboard())


@dispatcher.callback_query(lambda c: c.data.startswith('option'))
async def option(callback_query: CallbackQuery):
    options, button_text = callback_query.data.split(':')
    await callback_query.message.answer(f'Вы выбрали: {button_text}')
    await callback_query.answer()


@dispatcher.message(Command('dynamic'))
async def jokes(message: Message):
    await message.answer(text='Динамическое меню',reply_markup=kb.inline_keyboard_more)


@dispatcher.message(Command('forecast'))
async def wether_forecast(message: Message):
    city = 'Kaliningrad'
    city_ru = 'Калининград'
    weather = get_weather(city, city_ru)
    await message.answer(weather)


@dispatcher.message(Command('photo'))
async def photo(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    photo_list =['https://avatars.mds.yandex.net/i?id=d42bb4fccc692c80c905a00ab0d7e1aa3b673f35-9856182-images-thumbs&n=13',
                 'https://yandex.ru/images/search?source=related-0&text=улицы+калининграда&pos=1&rpt='
                 'simage&nomisspell=1&img_url=https%3A%2F%2Fsun9-79.userapi.com%2Fs%2Fv1%2Fif1%2F6VEk13scq5OndMVX_'
                 'iff1yFuUq_36bxC0yqgl9YrPQsgZ5-UvgeIpXpkm5IwsDAnlyWjRl1R.jpg%3Fsize%3D604x340%26quality%3D96'
                 '%26type%3Dalbum&from=tabbar&lr=117683',
                 'https://yandex.ru/images/search?p=1&source=related-0&text=улицы+калининграда&pos=2&rpt=simage&nomisspell=1&img_url=https%3A%2F%2Fpro-dachnikov.com%2Fuploads%2Fposts%2F2021-10%2F1633497152_3-p-dom-v-kaliningrade-foto-3.jpg&from=tabbar&lr=117683',
                 'https://yandex.ru/images/search?p=1&source=related-0&text=улицы+калининграда&pos=24&rpt=simage&nomisspell=1&img_url=https%3A%2F%2Fpp.userapi.com%2Fc844720%2Fv844720275%2Fb597%2FUdbQpFm5UTA.jpg&from=tabbar&lr=117683',
                 'https://yandex.ru/images/search?p=1&source=related-0&text=улицы+калининграда&pos=28&rpt=simage&nomisspell=1&img_url=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F3a%2Fde%2Fb3%2F3adeb380cf5aed12f4029ccccb80b95e.jpg&from=tabbar&lr=117683']
    await message.answer_photo(photo=choice(photo_list), caption='Калинград - это мой любимый город')


@dispatcher.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('media/video/video-1.mp4')
    await bot.send_video(message.chat.id, video)


@dispatcher.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('media/audio/my_song-1.mp3')
    await bot.send_audio(message.chat.id, audio)


@dispatcher.message(Command('training'))
async def training(message: Message):
    training = choice(TRAININGS)
    await message.answer(f'Это Ваша тренировка на сегодня - {training}')
    tts = gTTS(text=training, lang='ru')
    tts.save('tmp/audio/training.mp3')
    audio = FSInputFile('tmp/audio/training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove('tmp/audio/training.mp3')


@dispatcher.message(Command('voice'))
async def voice(message: Message):
    directory = 'tmp/voice_message/'
    voice_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not voice_files:
        await message.answer("Нет сохраненных голосовых сообщений.")
        return
    voice_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    last_voice_file = os.path.join(directory, voice_files[-1])
    voice = FSInputFile(last_voice_file)
    await message.answer_voice(voice)


@dispatcher.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Меня зовут Ларс и я Бот! С большой буквы!! '
                         f'Вы можете отправить мне фото и я скажу свое мнение о нем. Если Вы просто введете текст'
                         f' я переведу его на дргой язык', reply_markup=kb.main)


@dispatcher.message()
async def text(message: Message):
    inp_text = message.text
    target_language = lang(inp_text)
    if not (target_language is None):
        text = translate_text(inp_text)
        tts = gTTS(text=text, lang=target_language)
        tts.save('tmp/audio/translate.mp3')
        audio = FSInputFile('tmp/audio/translate.mp3')
    else:
        audio = FSInputFile('media/audio/unknown.wav')
    await message.answer(text)
    await bot.send_audio(message.chat.id, audio)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
