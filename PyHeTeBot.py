import requests
import telepot
import time
from emoji import emojize
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import variables


def on_chat_message(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/start':
        message = 'Start'
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=command), KeyboardButton(text='/roll')],
                                                 [KeyboardButton(text='/start'), KeyboardButton(text='4')]])
    elif command == '/roll':
        message = 'Roll'
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=emojize(':crossed_swords: 3 :shield: 3'), callback_data='risk'),
                 InlineKeyboardButton(text=emojize(':crossed_swords: 2 :shield: 2'), callback_data='risk')],
                [InlineKeyboardButton(text=emojize(':crossed_swords: 3 :shield: 2'), callback_data='risk'),
                 InlineKeyboardButton(text=emojize(':crossed_swords: 2 :shield: 1'), callback_data='risk')],
                [InlineKeyboardButton(text=emojize(':crossed_swords: 3 :shield: 1'), callback_data='risk'),
                 InlineKeyboardButton(text=emojize(':crossed_swords: 1 :shield: 1'), callback_data='risk')]])
    else:
        url_gtt = "http://gpa.madbob.org/query.php?stop=" + command
        req = requests.get(url_gtt).json()
        message = 'Fermata ' + command + '\n'
        lines = {}
        for bus in req:
            rt_char = ''  # realtime char
            if bus['realtime'] == 'true':
                rt_char = '*'
            if bus['line'] not in lines:
                lines[bus['line']] = rt_char + bus['hour'] + rt_char
            else:
                lines[bus['line']] += ' ' + rt_char + bus['hour'] + rt_char
        for line in lines.keys():
            message += '\nLinea ' + line + '\n' + lines[line]

        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=command), KeyboardButton(text='/roll')],
                                                 [KeyboardButton(text='3'), KeyboardButton(text='4')]])
    bot.sendMessage(chat_id, message, 'Markdown', reply_markup=keyboard)
    print 'Got command: %s' % command


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    if query_data == 'risk':
        bot.answerCallbackQuery(query_id, text='Risk')
        bot.editMessageText(msg['inline_message_id'], msg['data'])


bot = telepot.Bot(variables.TOKEN_BOT)

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print 'I am listening ...'

while 1:
    time.sleep(10)
