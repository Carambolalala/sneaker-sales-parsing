import telebot
from telebot import types
#from ..parser.links import parsingCore
#from ..parser.parser import parsing

TOKEN = 'BOT_API_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    CHAT_ID = message.from_user.id
    inlineMarkup = types.InlineKeyboardMarkup()

    #Начало списка маркетплейсов
    coreLink_1 = types.InlineKeyboardButton(text='Lamoda', url='https://www.lamoda.ru/')
    inlineMarkup.add(coreLink_1)
    #Конец списка маркетплейсов

    #Начало списка кнопок функций
    buttonMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Помощь')
    button2 = types.KeyboardButton('Поиск')
    buttonMarkup.add(button1, button2)
    #Конец списка кнопок функций

    startMessage = 'Данный бот - интерфейс для парсинга. Используемые маркетплейсы ниже. Для справки воспользуйтесь кнопкой Помощь'
    bot.send_message(CHAT_ID, startMessage, reply_markup=inlineMarkup)
    bot.send_message(CHAT_ID, 'Выберете, что ходите сделать:', reply_markup=buttonMarkup)

@bot.message_handler(content_types=['text'])
def getOption(message):
    CHAT_ID = message.from_user.id
    #Прописываем всю справку здесь
    if message.text == 'Помощь':
        helpText = 'Этот бот может искать скидки выбранных брендов кроссовок. ' \
                   'Для этого нажмите кнопку "Поиск" ниже. ' \
                   'После вам выдаст список категорий, которые вы хотите найти, в формате [бренд]-[пол]. ' \
                   'Выберете необходимые категории и начните поиск'
        bot.send_message(CHAT_ID, helpText)
    #Использование функций парсинга
    elif message.text == 'Поиск':
        pass
        buttons = {}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #ПРОДОЛЖЕНИЕ 

bot.polling(none_stop=True, interval=0)