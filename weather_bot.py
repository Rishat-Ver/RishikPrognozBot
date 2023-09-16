import os
import pyowm 
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
owm = pyowm.OWM(token, language='ru')
botToken = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(botToken)


@bot.message_handler(commands=['start'])
def start_work(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        obs = owm.weather_at_place(message.text)
        weather = obs.get_weather()
        temp = weather.get_temperature("celsius").get('temp')
        answer = f'В городе {message.text.title()} сейчас {weather.get_detailed_status()}'
        answer += f'\nТемпература:  {str(temp)}°C\n'
    except Exception as error:
        print(error)
        answer = 'Не найден такой город'
    bot.send_message(message.chat.id, answer)



bot.polling(none_stop=True)