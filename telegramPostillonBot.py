#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
#
# A simple Telegram bot (via getUpdates), crawling newstickers of the satirical
# news si www.postillon.de; answering always with the newest newstickers.
# Copyright (c) 2015 Robert Greinacher, development@robert-greinacher.de
#
# This program expects a 'config.py' file in the same directory.
# Rename the 'example_config.py' to 'config.py' and enter values
# according to your Telegram bot.



import config
import urllib.parse
import urllib.request
import json
import argparse
import sys
from dataManager import DataManager
from postillonCrawler import PostillonCrawler
from daemonize import Daemonize
from time import sleep



# defining constants and globals:
BE_VERBOSE = False
KNOWN_COMMANDS = ['/news', '/stats', '/help', '/description']
API_URL_BASE = 'https://api.telegram.org/bot'
API_URL = API_URL_BASE + config.AUTH_TOKEN
API_POLL_INTERVAL = 1
API_CALL_GET_UPDATES = 'getUpdates'
API_CALL_SEND_MESSAGE = 'sendMessage'



class TelegramPostillonBot:
  def __init__(self):
    self.postillon_crawler = PostillonCrawler(verbosity = BE_VERBOSE)
    self.data_manager = DataManager()
    self.last_request_id = 0

    self.start_polling_loop()

  def cleanup(self):
    self.data_manager.cleanup()

  def start_polling_loop(self):
    if BE_VERBOSE: print('start polling loop...')
    while True:
      try:
        parameters = {
          'offset': self.last_request_id + 1,
          'timeout': 1
        }
        requests = self.perform_api_call(API_CALL_GET_UPDATES, parameters)

        if (requests != False):
          for request in requests:
            chat_id, command = self.parse_message_object(request['message'])

            if command in KNOWN_COMMANDS:
              if BE_VERBOSE:
                print('received "', command, '" from chat_id ', chat_id)
              self.respond_to_request(chat_id, command)

            if request['update_id'] > self.last_request_id:
              self.last_request_id = request['update_id']

        else:
          if BE_VERBOSE:
            print('no requests, wait for ' + str(API_POLL_INTERVAL) + 's')
          sleep(API_POLL_INTERVAL)

      except KeyboardInterrupt:
        if BE_VERBOSE: print('Terminate bot because of keyboard interruption')
        self.cleanup()
        sys.exit(0)

      except:
        print('Uncatched error in run loop; terminating bot!')
        self.cleanup()
        sys.exit(0)

  def perform_api_call(self, function, parameters={}):
    parsed_parameters = urllib.parse.urlencode(parameters)
    encoded_parameters = parsed_parameters.encode('utf-8')

    try:
      # if BE_VERBOSE:
      #   print('requesting API with parameters: ' + parsed_parameters)

      request = urllib.request.Request(
        API_URL + '/' + function, encoded_parameters)

      response = urllib.request.urlopen(request).read()
      decoded_response = json.loads(response.decode('utf-8'))

      if decoded_response['ok'] == True:
        return decoded_response['result']
      else:
        if BE_VERBOSE: print('API error, bad respond code')

    except:
      if BE_VERBOSE: print('Uncatched error while requesting the bot API')

    return False

  def parse_message_object(self, message):
    chat_id = -1
    command = ''

    # save the received message to the DB
    self.data_manager.new_message(message)

    if 'chat' in message:
      chat_id = message['chat']['id']
    elif BE_VERBOSE:
      print('no chat object in responded message. \
        Unable to identify user or group to respond to.')

    if 'text' in message:
      command = message['text']

    return chat_id, command

  def respond_to_request(self, chat_id, command):
    data = {'chat_id': chat_id}
    if command == KNOWN_COMMANDS[0]:
      if BE_VERBOSE: print('responding with newsticker')
      self.postillon_crawler.check_for_updates()
      data['text'] = self.data_manager.get_newsticker_for_chat(chat_id)
    elif command == KNOWN_COMMANDS[1]:
      if BE_VERBOSE: print('responding with statistics')
      chats, newsticker, requests = self.data_manager.get_stistic()
      data['text'] = 'I answered ' + str(requests) + ' requests from '
      data['text'] += str(chats) + ' people and I know '
      data['text'] += str(newsticker) + ' headlines!'
    else:
      if BE_VERBOSE: print('responding with help text')
      data['text'] = self.create_information_respnse()

    self.perform_api_call(API_CALL_SEND_MESSAGE, data)

  def create_information_respnse(self):
    return '++++ Unofficial Postillon bot: \
      Use "/news" to get a new newsticker headline or \
      "/stats" to get an usage statistic ++++'



# ************************************************
# non object orientated entry code goes down here:
# ************************************************

def main():
  postillon_bot_instance = TelegramPostillonBot()
  # postillon_bot_instance.start()

# check if this code is run as a module or was included into another project
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description = "Polling Telegram bot (via getUpdates); \
      serving the Postillon newsticker")

  parser.add_argument(
    "-d", "--daemon",
    action = "store_true",
    dest = "daemon",
    help = "runs this bot as a daemon in the background")

  parser.add_argument(
    "-v", "--verbose",
    action = "store_true",
    dest = "verbose",
    help = "enables verbose mode")

  parser.add_argument(
    "-i", "--interval",
    type=int,
    help = "specifies the API polling interval in seconds")

  args = parser.parse_args()

  if args.verbose:
      BE_VERBOSE = True

  if args.interval:
      API_POLL_INTERVAL = args.interval
      if BE_VERBOSE:
        print('set API poll interval to ' + str(API_POLL_INTERVAL) + ' seconds')

  if args.daemon:
    if BE_VERBOSE:
        print('run in deamon mode... (verbose mode will not be helpful)')

    pidFile = "/tmp/telegramPostillonBotDaemon.pid"
    daemon = Daemonize(
      app='Telegram Postillon bot Daemon',
      pid=pidFile,
      action=main)
    daemon.start()
  else:
      main()
