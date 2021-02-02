import telebot
from telebot import types
import telegram
import time
import config
import random

token = config.token
bot = telebot.TeleBot(token)

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    a = types.KeyboardButton('1️⃣ Сложение и вычитание')
    b = types.KeyboardButton('2️⃣ Умножение и деление')
    c = types.KeyboardButton('3️⃣ Возведение в квадрат')
    d = types.KeyboardButton("4️⃣ Текстовая задача")
    markup.add(a, b, c,d)
    return markup

@bot.message_handler(commands=['start', 'начать', 'ready'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        'Добро пожаловать в наш бот\n'
        'В появившемся окне вам следует выбрать тип задачи\n'
        '1️⃣-ая кнопка выдаст задачу на сложение или вычитание с числами от 1 до 1000\n'
        '2️⃣-ая кнопка выдаст задачу на умножение или деление с числами от 1 до 100\n'
        '3️⃣-ая кнопка выдаст задачу на возведение числа в квадрат для чисел от 1 до 20\n'
        '4️⃣-ая кнопка выдаст текстовую задачу на логику\n'
        'После решения задачи, отправляем боту ответ в виде числа(никаких других знаков)\n'
        'В случае неправильного ответа, бот вам сообщит об ошибке, и отправит правильный '
        'ответ',
        reply_markup = keyboard())

@bot.message_handler(content_types=["text"])
def question1(message):
    send = None
    txt = message.text
    global answer
    if txt == '1️⃣ Сложение и вычитание':
        a = random.randint(500,1000)
        b = random.randint(0,500)
        c = random.choice(['-','+'])
        bot.send_message(chat_id, "{} {} {} = ?".format(a, c, b))
        if c == '-':
            answer = a - b
            send = bot.send_message(chat_id, 'Введите результат вычитания: ')
        else:
            answer = a + b
            send = bot.send_message(chat_id, 'Введите результат сложения: ')
    elif txt == "2️⃣ Умножение и деление":
        a = random.randint(50,100)
        b = random.randint(1,50)
        c = random.choice(['/', '*'])
        bot.send_message(chat_id, "{} {} {} = ?".format(a,c,b))
        if c == '/':
            answer = a // b
            send = bot.send_message(chat_id, 'Введите целую часть от деления:')
        else:
            answer =  a * b
            send = bot.send_message(chat_id, 'Введите результат умножения: ')
    elif txt == "3️⃣ Возведение в квадрат":
        a = random.randint(1,20)
        bot.send_message(chat_id, "{} в квадрате = ?".format(a))
        answer = pow(a,2)
        send = bot.send_message(chat_id, "Введите результат возведения числа в квадрат: ")
    elif txt == "4️⃣ Текстовая задача":
        a = random.randint(0,10)
        bot.send_message(chat_id, "{}".format(config.spisok[a]))
        send = bot.send_message(chat_id, 'Введите ответ задачки: ')
        answer = config.spisok[a+10]
    bot.register_next_step_handler(send, answer1)

def answer1(message):
    global txt
    txt = message.text
    send = bot.send_message(chat_id, 'И так: ')
    time.sleep(2)
    if txt.isdigit() and int(txt) == answer:
        bot.send_message(chat_id, 'Отлично!\nВы ввели правильный ответ')
    else:
        bot.send_message(chat_id, 'Вы ввели неправильный ответ\n'
                                  'Правильный ответ: {}'.format(answer))
bot.polling()
