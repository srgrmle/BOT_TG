import telebot
from g4f.client import Client
import requests
from bs4 import BeautifulSoup
from textwrap import wrap

# Замените TOKEN на ваш реальный токен
TOKEN = '8060008644:AAFhlvsHVtoh-ZjO_1kttBhxUqrDDjIAWz8'
bot = telebot.TeleBot(TOKEN)


# Функция для обработки команд /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}')


# Функция для обработки текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    client = Client()
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': message.text}]
    )
    bot.send_message(message.chat.id, response.choices[0].message.content)


# Функция для получения краткого содержания веб-страницы
def generate_summary(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f'Ошибка при получении страницы: статус-код {response.status_code}')

        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = soup.get_text(strip=True)

        prompt = 'Сделайте краткое содержание по этой странице. Выберите только самое важное.'
        prompt += page_content

        client = Client()
        response = client.chat.completions.create(
            model='gpt-4-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )
        summary = response.choices[0].message.content

        return summary
    except Exception as e:
        return str(e)


# Команда для генерации краткого содержания
@bot.message_handler(commands=['summary'])
def send_summary(message):
    url = message.text.split(maxsplit=1)[1]
    summary = generate_summary(url)
    for line in wrap(summary, width=65):
        bot.send_message(message.chat.id, line)


# Запуск бота
bot.polling()

