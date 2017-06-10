#!/usr/bin/env python27
# coding:utf-8

# Modules
import os  # system library needed to read the environment variables
import requests  # library to make requests to telegram server
import json  # library for evaluation of json file

TOKEN_BOT = os.environ.get('TOKEN_BOT')  # Telegram token for the bot API


class BotHandler:
    """ class with method used by the bot, for more details see
        https://core.telegram.org/bots/api
    """

    def __init__(self, token):
        """ init function to set bot token and reference url
        """
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        # set bot url from the token

    def get_updates(self, offset=None, timeout=30):
        """ method to receive incoming updates using long polling
            [Telegram API -> getUpdates ]
        """
        params = {'offset': offset, 'timeout': timeout}
        return requests.get(self.api_url + 'getUpdates',
                            params).json()['result']  # return an array of json

    def send_message(self, chat_id, text, parse_mode='Markdown',
                     disable_web_page_preview=True):
        """ method to send text messages [ Telegram API -> sendMessage ]
        """
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode,
                  'disable_web_page_preview': disable_web_page_preview}
        return requests.post(self.api_url + 'sendMessage', params)  # On success, the sent Message is returned.

    def get_last_update(self):
        """method to get last message if there is"""
        get_result = self.get_updates()  # recall the function to get updates
        if len(get_result) > 0:  # check if there are new messages
            return get_result[-1]  # return the last message in json format
        else:
            return -1
            # in case of error return an error code used in the main function


# set variable used in main function
pyhetebot = BotHandler(TOKEN_BOT)  # create the bot object


def main():
    new_offset = None  # set at beginning an offset None for the get_updates function

    while True:
        pyhetebot.get_updates(new_offset)
        # call the function to check if there are new messages
        last_update = pyhetebot.get_last_update()
        # takes the last message from the server

        if last_update != -1:
            try:
                user_file = json.loads("http://gpa.madbob.org/query.php?stop=")

                last_update_id = last_update['update_id']
                # store the id of the bot taken from the message
                new_offset = last_update_id + 1
                # store the update id of the bot
                command = last_update['message']['text']
                # store all the words in the message in an array
                # (split by space)
                last_chat_id = last_update['message']['chat']['id']
                # store the id of the chat between user and bot read from
                # the message in a variable
                last_user_id = last_update['message']['from']['id']
                # store the id of the user read from the message in a variable
                last_user_name = last_update['message']['from']['first_name']
                # store the name of the user read from the message
                # in a variable
                last_user_username = last_update['message']['from']['username']
                # store the username of the user read from the message
                # in a variable
                message_type = last_update['message']['chat']['type']

                pyhetebot.send_message(last_chat_id, command)

            except KeyError:  # catch the exception if raised
                print "ERROR!"  # DEBUG


# call the main() until a keyboard interrupt is called
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
