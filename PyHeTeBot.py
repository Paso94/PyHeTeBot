import requests
import telepot
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import variables


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

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

    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=command)]])
    bot.sendMessage(chat_id, message, 'Markdown', reply_markup=keyboard)

    print 'Got command: %s' % command


bot = telepot.Bot(variables.TOKEN_BOT)

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

while 1:
    time.sleep(10)
