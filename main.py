import telebot
import config
from telebot import types
import sqlite3

def word_checker(string,words):
    string = string.lower()
    n = 0
    for word in words:
        if word in string:
            n += 1
    if n > 0:
        return True
    else:
        return False

bot = telebot.TeleBot(config.token);

conn = sqlite3.connect("user_info.db",check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    UserID INT PRIMARY KEY,
    UserName TEXT,
    UserProf TEXT,
    MessageEnabled INT);
""")
conn.commit()

dictionary = { "Дизайн" : ['#ищудизай','#сделатьдизайн'],
               "Программирование" : ['#ищуразработчик', '#ищупрограммис', '#ищуинжен'],
               "СММ" : ['смм','маркетолог'],
               "Таргет" : ['#ищутаргет', '#ищутаргетолог', '#настроитьтаргет', "таргет"]
             }

@bot.message_handler(commands=['start'])
def add_user(message):
    if message.chat.type == "private":
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton(text = 'Дизайн',callback_data = "/set_design" )
        itembtn2 = types.InlineKeyboardButton(text = 'Программирование',callback_data = "/set_prog" )
        itembtn3 = types.InlineKeyboardButton(text = 'СММ',callback_data = "/set_smm" )
        itembtn4 = types.InlineKeyboardButton(text = 'Таргет',callback_data = "/set_target" )
        itembtn5 = types.InlineKeyboardButton(text = 'Отмена',callback_data = "/cancel" )
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4,itembtn5)
        bot.send_message(message.chat.id, "Выберите желаемую специализацию",reply_markup = markup)
        
@bot.message_handler(commands=['edit'])
def enable_messages(message):
    if message.chat.type == "private":
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton(text = 'Да',callback_data = "/enable_message_sending" )
        itembtn2 = types.InlineKeyboardButton(text = 'Нет',callback_data = "/disable_message_sending" )
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Продолжить отправлять сообщения о вакансиях?",reply_markup = markup)
        

@bot.callback_query_handler(func = lambda call:True)
def callback(call):
    if call.data == "/set_design":
        bot.send_message(call.from_user.id, "Поиск вакансий изменен на 'Дизайн'")
        user = (call.from_user.id, call.from_user.username, "Дизайн", 1)
        cursor.execute("SELECT UserID FROM users WHERE UserID=?", (call.from_user.id,))
        exists = cursor.fetchall()
        if not exists:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
        else:
            cursor.execute("""UPDATE users SET UserProf=?
                              WHERE UserID=?
                              """, ("Дизайн", call.from_user.id))
    elif call.data == "/set_prog":
        bot.send_message(call.from_user.id, "Поиск вакансий изменен на 'Программирование'")
        user = (call.from_user.id, call.from_user.username, "Программирование", 1)
        cursor.execute("SELECT UserID FROM users WHERE UserID=?", (call.from_user.id,))
        exists = cursor.fetchall()
        if not exists:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
        else:
            cursor.execute("""UPDATE users SET UserProf=?
                              WHERE UserID=?
                              """, ("Программирование", call.from_user.id))
    elif call.data == "/set_smm":
        bot.send_message(call.from_user.id, "Поиск вакансий изменен на 'СММ'")
        user = (call.from_user.id, call.from_user.username, "СММ", 1)
        cursor.execute("SELECT UserID FROM users WHERE UserID=?", (call.from_user.id,))
        exists = cursor.fetchall()
        if not exists:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
        else:
            cursor.execute("""UPDATE users SET UserProf=?
                              WHERE UserID=?
                              """, ("СММ", call.from_user.id))
    elif call.data == "/set_target":
        bot.send_message(call.from_user.id, "Поиск вакансий изменен на 'Таргетолог'")
        user = (call.from_user.id, call.from_user.username, "Таргет", 1)
        cursor.execute("SELECT UserID FROM users WHERE UserID=?", (call.from_user.id,))
        exists = cursor.fetchall()
        if not exists:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
        else:
            cursor.execute("""UPDATE users SET UserProf=?
                              WHERE UserID=?
                              """, ("Таргет", call.from_user.id))
    elif call.data == "/cancel":
        bot.send_message(call.from_user.id, "Отмена")
    elif call.data == "/enable_message_sending":
        cursor.execute("SELECT UserID FROM users WHERE UserID=?", (call.from_user.id,))
        exists = cursor.fetchall()
        if not exists:
            bot.send_message(call.from_user.id, "Сначала выберите вид вакансии")
        else:
            cursor.execute("""UPDATE users SET MessageEnabled=?
                              WHERE UserID=?
                              """, (1, call.from_user.id))
            bot.send_message(call.from_user.id, "Отправка вакансий включена")
    elif call.data == "/disable_message_sending":
        cursor.execute("SELECT UserID FROM users WHERE UserID=?", (call.from_user.id,))
        exists = cursor.fetchall()
        if not exists:
            bot.send_message(call.from_user.id, "Сначала выберите вид вакансии")
        else:
            cursor.execute("""UPDATE users SET MessageEnabled=?
                              WHERE UserID=?
                              """, (0, call.from_user.id))
            bot.send_message(call.from_user.id, "Отправка вакансий отключена")
    bot.answer_callback_query(call.id)
    bot.delete_message(call.from_user.id, call.message.id)
    conn.commit()

@bot.channel_post_handler(content_types=['text'])
def echo_posts(*messages):
    for m in messages:
        if m.chat.type != "private":
            chatid = m.chat.id
            if m.content_type == "text":
                cursor.execute("SELECT UserID FROM users")
                users = cursor.fetchall()
                conn.commit()
                for user in users:
                    cursor.execute("SELECT UserProf, MessageEnabled FROM users WHERE UserID=?",user)
                    userData = cursor.fetchone()
                    conn.commit()
                    if word_checker(m.text, dictionary[userData[0]]) and userData[1] == 1 and word_checker(m.text, ['#ищу', 'нужен']):
                        text = m.text + ' \n'
                        bot.send_message(user[0], text + 'https://t.me/' + m.chat.username + '/' + str(m.message_id))

@bot.message_handler(content_types=['text'])
def echo_messages(*messages):
    for m in messages:
        if m.chat.type != "private":
            chatid = m.chat.id
            if m.content_type == "text":
                cursor.execute("SELECT UserID FROM users")
                users = cursor.fetchall()
                conn.commit()
                for user in users:
                    cursor.execute("SELECT UserProf, MessageEnabled FROM users WHERE UserID=?",user)
                    userData = cursor.fetchone()
                    conn.commit()
                    if word_checker(m.text, dictionary[userData[0]]) and userData[1] == 1 and word_checker(m.text, ['#ищу','нужен']):
                        text = m.text + " \n"
                        bot.send_message(user[0],text + '@' + m.from_user.username)
    

#bot.set_update_listener(echo_messages)
bot.polling(none_stop=True)

while True: # Don't let the main Thread end.
    pass