import telebot
from telebot import types
from parser.links import parsingCore
from parser.parser import parsing

TOKEN = 'BOT_API_TOKEN'
bot = telebot.TeleBot(TOKEN)


#Заготовка категорий
categoryButtons = {}
iButton = 1
for key in parsingCore:
    categoryButtons[iButton] = key
    iButton += 1
chosenCategories = []

#Глобальная переменная для корректной работы
foundSneakers = {}

#ЗАГОТОВКИ СТИЛЕЙ ДЛЯ БОТА
    #START, HELP >>>>
startMarkup = types.InlineKeyboardMarkup()
#Начало списка маркетплейсов
coreLink_1 = types.InlineKeyboardButton(text='Lamoda', url='https://www.lamoda.ru/')
startMarkup.add(coreLink_1)
#Конец списка маркетплейсов
#Начало списка кнопок функций
startButtonMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Помощь')
button2 = types.KeyboardButton('Поиск')
startButtonMarkup.add(button1, button2)
#Конец списка кнопок функций
startMessage = 'Данный бот - интерфейс для парсинга. Используемые маркетплейсы ниже. Для справки воспользуйтесь кнопкой Помощь'

    #ПОМОЩЬ >>>>
#Прописываем справку здесь
helpText = 'Этот бот может искать скидки выбранных брендов кроссовок.\n' \
           'Для этого: \n-Нажмите кнопку "Поиск" ниже.\n' \
           '-После вам выдаст список категорий, которые вы хотите найти, в формате [бренд]-[пол].\n' \
           '-Выберете необходимые категории и начните парсинг.\n-Напишите количество товаров, которое хотите вывести сейчас'

    #ПОИСК >>>>
categoriesInlineMarkup = types.InlineKeyboardMarkup(row_width=3)
#Создает inline-кнопки исходя из категорий в файле parser/links.py
for key in categoryButtons:
    categoriesInlineMarkup.add(types.InlineKeyboardButton(categoryButtons[key], callback_data=categoryButtons[key]))
startSearchMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
startSearchMarkup.add(types.KeyboardButton('Начать парсинг'))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    CHAT_ID = message.from_user.id
    bot.send_message(CHAT_ID, startMessage, reply_markup=startMarkup)
    bot.send_message(CHAT_ID, 'Выберете, что ходите сделать:', reply_markup=startButtonMarkup)

@bot.message_handler(content_types=['text'])
def getOption(message):
    CHAT_ID = message.from_user.id
    global foundSneakers
    global chosenCategories
    #Отправляет справку
    if message.text == 'Помощь':
        bot.send_message(CHAT_ID, helpText)
    #Отбор категорий для парсинга
    elif message.text == 'Поиск':
        bot.send_message(CHAT_ID, 'Выбери категории', reply_markup=categoriesInlineMarkup)
        bot.send_message(CHAT_ID, 'После нажми "Начать парсинг":', reply_markup=startSearchMarkup)
    #Запуск процесса парсинга
    elif message.text == 'Начать парсинг':
        if not chosenCategories:
            bot.send_message(CHAT_ID, 'Категории не выбраны!')
        else:
            bot.send_message(CHAT_ID, 'Работаю...', reply_markup=startButtonMarkup)
            foundSneakers = parsing(chosenCategories)
            bot.send_message(CHAT_ID, f'Найдено {len(foundSneakers)} товаров. Напиши, сколько вывести (Впиши 0 для отмены): ')
    else:
        if len(foundSneakers) > 0:
            try:
                chosenAmount = int(message.text)
                if chosenAmount == 0:
                    foundSneakers.clear()
                    chosenCategories.clear()
                    bot.send_message(CHAT_ID, 'Найденные товары очищены')
                elif chosenAmount > len(foundSneakers):
                    bot.send_message(CHAT_ID, 'Найденных товаров меньше!')
                else:
                    for category in chosenCategories:
                        for number in range(1, chosenAmount+1):
                            sneaker = foundSneakers[category + f'-{number}']
                            if sneaker.image == None: #Нужно на время, пока не исправлена ситуация с ограничением в 12 картинок
                                sneaker.image = 'i.pinimg.com/564x/9f/ab/e5/9fabe5f90ca53f9a86306203f517f9fd.jpg'
                            bot.send_photo(CHAT_ID, 
                                           sneaker.image,
                                            'Бренд: ' + category.split('-')[0] + '\n'\
                                            'Название: ' + sneaker.name + '\n'\
                                            'Старая цена: ' + sneaker.oldPrice + '\n'\
                                            'Новая цена: ' + sneaker.newPrice + '\n'\
                                            'Ссылка на товар: ' + sneaker.source)
                    foundSneakers.clear()
                    chosenCategories.clear()
                    bot.send_message(CHAT_ID, 'Отправил выбранное количество товаров')
            except ValueError:
                bot.send_message(CHAT_ID, 'Это не число!')
        else:
            bot.send_message(CHAT_ID, 'Такой команды нет!')
       
@bot.callback_query_handler(func=lambda c:True)
def getOption(inlineData):
    #Добавление выбранных категорий в список для парсинга
    if inlineData.data not in chosenCategories:
        chosenCategories.append(inlineData.data)

bot.polling(none_stop=True, interval=0)