# - *- coding: utf- 8 - *-
import telebot
from telebot import types
import pypyodbc


mydb = pypyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-3F59213;"
        "Database=Telebot;"
)
cursor = mydb.cursor()
mySQLQuery = ("""
                SELECT TOP 11 *
                FROM dbo.adresa
            """)

token = '1181992733:AAH79PQaMpHMJfazGSL4SZNLGSzdCWPc5Y4'
url = 'https://api.telegram.org/bot1181992733:AAH79PQaMpHMJfazGSL4SZNLGSzdCWPc5Y4/getUpdates'
user_dict = {}
bot = telebot.TeleBot(token)

class User:
    def __init__(self, adres):
        self.adres = adres

    def __str__(self):
        return self.adres


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    key_start = types.KeyboardButton("/start")
    key_add = types.KeyboardButton("/add")
    key_list = types.KeyboardButton("/list")
    key_reset = types.KeyboardButton("/reset")
    markup.add(key_start, key_add, key_list, key_reset)

    bot.send_message(message.chat.id, 'Привет я бот заметка, вы можете отправить piмне вашу заметку или посмотреть список сохраненых мест\n'
                                      'C помощью /add вы можете ввести адресс\n'
                                      'C помощью /list вы можете вывести сохраненные места\n'
                                      'C помощью /reset вы можете удалить данные', parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['add'])
def perehod(message):
        msg = bot.send_message(message.chat.id, 'Введите адрес')
        bot.register_next_step_handler(msg, zapis)

def zapis(message):
    try:
        id = message.from_user.id
        user_dict[id] = User(message.text)
        for i, j in user_dict.items():
            if id == i:
                cursor.execute("insert into [Telebot].[dbo].[Adresa] VALUES ('{0}', '{1}')".format(i, j))
                mydb.commit()
        bot.send_message(message.chat.id, 'Адрес сохранен')
    except Exception as e:
        bot.reply_to(message, 'oops')

@bot.message_handler(commands=['list'])
def vivod_adresa(message, j=0):
    cursor.execute(mySQLQuery)
    results = cursor.fetchall()
    for i in results:
        ids = i[0]
        adres = i[1]
        if ids == message.from_user.id:
            bot.send_message(message.chat.id, adres)
            print(adres)
        j += 1

@bot.message_handler(commands=['reset'])
def delete(message):
    cursor.execute(mySQLQuery)
    results = cursor.fetchall()
    for i in results:
        ids = i[0]
        if ids == message.from_user.id:
            cursor.execute("""DELETE FROM [Telebot].[dbo].[Adresa] WHERE id = {0}""".format(ids))
            mydb.commit()
    bot.send_message(message.chat.id, 'Адреса удалены')

if __name__ == '__main__':
    bot.polling(none_stop=True)