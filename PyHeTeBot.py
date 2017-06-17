import requests
import telepot
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import variables


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/start':
        message = 'Start'
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=command), KeyboardButton(text='/roll')],
                                                 [KeyboardButton(text='3'), KeyboardButton(text='4')]])
    elif command == '/roll':
        message = 'Roll'
        keyboard = InlineKeyboardMarkup(keyboard=[[InlineKeyboardButton(text=' '), InlineKeyboardButton(text=command)],
                                                  [InlineKeyboardButton(text='3'), InlineKeyboardButton(text='4')]])
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

        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=command), KeyboardButton(text='2')],
                                                 [KeyboardButton(text='3'), KeyboardButton(text='4')]])
    bot.sendMessage(chat_id, message, 'Markdown', reply_markup=keyboard)

    print 'Got command: %s' % command


bot = telepot.Bot(variables.TOKEN_BOT)

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

while 1:
    time.sleep(10)
