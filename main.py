import telebot
from telebot import types
from config import *
from utils import *


def create_markup(base = None):
       markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
       buttons = []

       for var in exchange.keys():
              if var != base:
                     buttons.append(types.KeyboardButton(var.capitalize()))
       markup.add(*buttons)

       return markup

bot_exchange = telebot.TeleBot(TOKEN)


@bot_exchange.message_handler(commands=['start'])
def manual_exchange(message: telebot.types.Message):
       text = f"Здравствуйте, {message.chat.first_name}. \n\n"\
"Я бот валют по текущему курсу. Введите через пробел: \n\n" \
"<исходная валюта> <целевая валюта> <сумма для обмена> \n\n" \
"или воспользуйтесь командой /convert \n\n" \
"/help для подробного списка команд."
       bot_exchange.reply_to(message, text)

@bot_exchange.message_handler(commands=['help'])
def handle_help(message):
       str_ = "*Перечень допустимых команд\:* \n\n"\
"Общее описание бота \- /start\n"\
"Данный список команд \- /help\n"\
"Список доступных мне валют \- /values"
       bot_exchange.send_message(message.chat.id, str_, parse_mode='MarkdownV2')


@bot_exchange.message_handler(commands=['values'])
def values_exchange(message: telebot.types.Message):
       text = 'Доступные валюты:'
       for i in exchange.keys():
           text = '\n'.join((text, i))
       bot_exchange.reply_to(message, text)


@bot_exchange.message_handler(commands=['convert'])
def values_exchange(message: telebot.types.Message):
       text = 'Выберете валюту из которой конвертировать:'
       bot_exchange.send_message(message.chat.id, text, reply_markup=create_markup())
       bot_exchange.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
       base = message.text.strip().lower()
       text = 'Выберете валюту в которую хотите конвертировать:'
       bot_exchange.send_message(message.chat.id, text, reply_markup=create_markup(base))
       bot_exchange.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
       sym = message.text.strip().lower()
       text = 'Выберете количество конвертируемой валюты:'
       bot_exchange.send_message(message.chat.id, text)
       bot_exchange.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
       amount = message.text.strip()
       try:
              new_price = Converter.get_price(base, sym, amount)
       except APIException as e:
              bot_exchange.send_message(message.chat.id, f'Ошибка конвертации\n{e}')
       else:
              text = f'Стоимость {amount} {base} в {sym} составляет {new_price}'
              bot_exchange.send_message(message.chat.id, text)

@bot_exchange.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
       try:
              comands = message.text.split()
              if len(comands) != 3:
                     raise ValueError('Неверное количество параметров')
              base, sym, amount = comands
              new_price = Converter.get_price(base, sym, amount)
              bot_exchange.reply_to(message,
                                    f'Стоимость {amount} {base} в {sym} составляет {new_price}')
       except APIException as e:
              bot_exchange.reply_to(message, f"{e}")
       except Exception as e:
              bot_exchange.reply_to(message, f"{e}")

@bot_exchange.message_handler(content_types=['audio', ])
def audio_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Сочный звук, мне нра. Хотя ОЙ, ушей-то у меня нет. Вру.')


@bot_exchange.message_handler(content_types=['photo', ])
def photo_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Для меня картинки все на одну точку, ничего не вижу, глаз-то нет.')


@bot_exchange.message_handler(content_types=['voice', ])
def voice_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Я робот, мной непостижимы голоса из внешнего мира.')


@bot_exchange.message_handler(content_types=['video', ])
def video_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Что-то мельтешит такое, но не распознаю. Я-ж не нейросеть, робот простой.')


@bot_exchange.message_handler(content_types=['document', ])
def doc_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Видать что-то дельное написано. Но мне не понять, я больше по валютам.')


@bot_exchange.message_handler(content_types=['location', ])
def loc_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Теперь я знаю, где вы находитесь. Но мне это знание бесполезно, уже забыл.')

@bot_exchange.message_handler(content_types=['contact', ])
def cont_factory(message: telebot.types.Message):
    bot_exchange.send_message(message.chat.id, 'Будь у меня мозги, я-б пообщался. Но я не Страшила-Мудрый, мне нечем думать.')

@bot_exchange.message_handler(content_types=['sticker'])
def stic_factory(message: telebot.types.Message):
    bot_exchange.send_sticker(message.chat.id, "CAACAgIAAxkBAAOMY6WAdMw1TO1RLiHv6M807AcmZgsAAh4AA8A2TxOhYFstqwAB3gQsBA")

bot_exchange.polling()