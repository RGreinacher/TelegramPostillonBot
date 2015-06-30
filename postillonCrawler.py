#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

# Postillon crawler. An object of this class will request the
# Postillon newsticker page every POSTILLON_CRAWLING_INTERVAL seconds,
# will extract the newsticker and make them accessible via the
# get_next_newsticker() method.
# This code is a relict of an old quote-of-the-day-server project
#
# TODOs:
# - use BeautifulSoup to extract the newsticker
# - recognize an ID of the one who is requesting to avoid the global
#   "current-headline-pointer"
#
# Copyright (c) 2015 Robert Greinacher, development@robert-greinacher.de



import urllib3
import re
import sys
import hashlib
import datetime
from dataManager import DataManager



# defining constants and globals:
BE_VERBOSE = False
POSTILLON_CRAWLING_INTERVAL = 60 * 60 * 2



class PostillonCrawler:
  def __init__(self, verbosity = False):
    self.data_manager = DataManager()
    self.last_update_timestamp = 0
    self.latest_headline_hash = 0
    self.headlines = []
    self.web_encoding = 'UTF-8'

    BE_VERBOSE = verbosity
    self.update_newsticker()

  def get_next_newsticker(self):
    self.check_for_updates()
    return next(self.headlines)

  def check_for_updates(self):
    offset = self.get_current_timestamp() - self.last_update_timestamp
    if offset > POSTILLON_CRAWLING_INTERVAL:
      self.update_newsticker()

  def update_newsticker(self):
    if BE_VERBOSE: print("PostillonCrawler: update newsticker")

    news_list = self.get_newsticker_rows()
    if news_list == []:
      return False

    self.last_update_timestamp = self.get_current_timestamp()
    testHash = hashlib.md5(news_list[0]).hexdigest()
    if self.latest_headline_hash == testHash:
      return False

    # create new array of headline objects
    self.headlines = [self.ticker_formatter(line) for line in news_list]

    # save the new newsticker to the DB
    self.data_manager.new_newsticker(self.headlines)

    # update headline hash to differenciate newsticker
    self.latest_headline_hash = testHash

    if BE_VERBOSE: print('PostillonCrawler: ',
      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      ' headlines are up to date')

  def get_newsticker_rows(self):
    http = urllib3.PoolManager()

    try:
      request_result = http.request('GET',
        'http://www.der-postillon.com/search/label/Newsticker')

      try:
        content_type = request_result.headers['content-type']
        encoding_start_position = content_type.find('charset=') + 8
        self.web_encoding = content_type[encoding_start_position:]
      except AttributeError:
        self.web_encoding = 'UTF-8'

      text = request_result.data
      news_list = re.findall(
        '\+\+\+\+\ (.*?)\ \+\+\+\+'.encode(self.web_encoding), text)

    except:
      if BE_VERBOSE: print("ERROR: can\'t get any headlines from Postillon!")
      return []

    return news_list

# PRAGMA MARK: - helper

  def ticker_formatter(self, news_row):
      return "++++ {} ++++\n".format(news_row.decode('UTF-8'))

  def get_current_timestamp(self):
    now = datetime.datetime.now()
    then = datetime.datetime(1970, 1, 1)
    return int((now - then).total_seconds())
