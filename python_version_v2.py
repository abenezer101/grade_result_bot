import telebot
from telebot import types
import mysql.connector
from flask import Flask, request

################################### TelegramBot frontend code starts here ##########################################

bot = telebot.TeleBot('6513187968:AAFO5TW6aBv9z8lIp4sPTACFj4VucGGNs-Q')
URL="https://opis-results-bot.vercel.app/"

users=set()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('View grade')
    itembtn2 = types.KeyboardButton('Help')
    itembtn3 = types.KeyboardButton('Stats')
    itembtn4 = types.KeyboardButton('About')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4 )

    users.add(message.from_user.id)

    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}, welcome to the grade report system!", reply_markup=markup)

@bot.message_handler(commands=['contact_support'])
def Contact_us(message):
    bot.reply_to(message, "You can contact us here @CyberhnterX")

@bot.message_handler(commands=['view_grade'])
def view_grade(message):
    bot.reply_to(message, "Enter you personal information based on this forma >> UserName Password Subject Assesment")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "To use this bot, Click on /view_grade \n then enter your personal details personal details required: \n \n        * Username (Given by admin)\n        * Password (Given by admin)\n        * Subject (Course you are taking)\n        * Assessment (usually Test / Quiz )\n \nClick /contact_support to contact the admin")


@bot.message_handler(func=lambda message: message.text == 'View grade')
def command_view_grade(message):
    bot.reply_to(message, "Enter you personal information based on this format >> UserName Password Subject Assesment")

@bot.message_handler(func=lambda message: message.text == 'Help')
def command_help(message):
    bot.reply_to(message, "To use this bot, Click on /view_grade \n then enter your personal details personal details required: \n \n        * Username (Given by admin)\n        * Password (Given by admin)\n        * Subject (Course you are taking)\n        * Assessment (usually Test / Quiz )\n \nClick /contact_support to contact the admin")

@bot.message_handler(func=lambda message: message.text == 'Stats')
def command_stats(message):
    bot.reply_to(message, f"The bot is currently being used by {len(users)} user(s).")

@bot.message_handler(func=lambda message: message.text == 'About')
def command_about(message):
    bot.reply_to(message, "Our result broadcasting Telegram bot streamlines the process of accessing grades for students and teachers. It provides a convenient and efficient way to post and check grades through the Telegram platform, eliminating the need for manual access to separate systems or websites.\n \nmade by Abenezer.A & Abdulhakim.A")

################################### TelegramBot frontend code Ends here ##########################################

#################################### Mysql database connection and processing code starts here ###################
# Connect to MySQL database
mydb = mysql.connector.connect(
   host="db4free.net",
   port="3306",
   user="results_bot",
   password="Abenezerabera321##",
   database="opisgradedb"
# host="localhost",
# user="root",
# password="",
# database="opis grade reporter"
)
# Create a cursor object to interact with the database
mycursor = mydb.cursor()

# # Handle messages with username, password, and subject
# @bot.message_handler(func=lambda message: True)
# def process_message(message):
#     chat_id = message.chat.id
#     text = message.text.split()
#     if len(text) == 3:
#         username, password, subject = text
#         query = "SELECT * FROM users WHERE username = %s AND password = %s AND subject = %s"
#         values = (username, password, subject)
#         mycursor.execute(query, values)
#         result = mycursor.fetchone()
#         if result:
#             bot.send_message(chat_id, result[3])
#         else:
#             bot.send_message(chat_id, "Invalid credentials.")
#     else:
#         bot.send_message(chat_id, "Please enter username, password, and subject.")




def fetch_user_result(username: str, password: str, subject: str):
    query = "SELECT * FROM users WHERE username = %s AND password = %s AND subject = %s"
    values = (username, password, subject)
    mycursor.execute(query, values)
    result = mycursor.fetchone()
    return result

WAIT_MESSAGE = "Please wait a moment while I'm checking your result."

@bot.message_handler(regexp=r"^(\w+)\s+(.+)\s+(\w+)$")
def handle_message(message: telebot.types.Message):
    name, passwd, subject = message.text.split()
    msg = bot.reply_to(message, WAIT_MESSAGE)
    result = fetch_user_result(name, passwd, subject)
    bot.edit_message_text(WAIT_MESSAGE + ".", message.chat.id, msg.message_id)
    if not result:
        bot.edit_message_text(
            f"Sorry, your credential is incorrect. Please try again.",
            message.chat.id,
            msg.message_id,
        )
        return
    bot.reply_to(message, f"Hello {name}, your result for {subject} is {result[3]}.")
    bot.delete_message(message.chat.id, msg.message_id)
    
    
bot.polling()


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/{}'.format(bot), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=host, HOOK=bot))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


