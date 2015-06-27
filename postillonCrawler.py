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



# defining constants and globals:
BE_VERBOSE = False
POSTILLON_CRAWLING_INTERVAL = 60 * 30



class Headline:
  def __init__(self, headline):
    self.headline = headline

  def __str__(self):
    return "++++ {} ++++\n".format(self.headline.decode('UTF-8'))



class PostillonCrawler:
  def __init__(self, verbosity = False):
    self.last_update_timestamp = 0
    self.latest_headline_hash = 0
    self.headlines = []
    self.web_encoding = 'UTF-8'

    BE_VERBOSE = verbosity
    self.update_newsticker()

  def get_next_newsticker(self):
    offset = self.get_current_timestamp() - self.last_update_timestamp
    if offset > POSTILLON_CRAWLING_INTERVAL:
      self.update_newsticker()
    return next(self.headlines)

  def update_newsticker(self):
    if BE_VERBOSE: print("PostillonCrawler: update newsticker")
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

    except AttributeError:
      if BE_VERBOSE: print("Can\'t get any headlines from Postillon! \
        Error handling would be great!")
      sys.exit(0)

    self.last_update_timestamp = self.get_current_timestamp()
    testHash = hashlib.md5(news_list[0]).hexdigest()
    if self.latest_headline_hash == testHash:
      return

    def headline_converter():
      while 1:
        for headline in headlines:
          yield str(headline)

    # create array ob headline objects
    headlines = [Headline(line) for line in news_list]
    self.headlines = headline_converter()
    self.latest_headline_hash = testHash

    if BE_VERBOSE: print('PostillonCrawler: ',
      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      ' headlines are up to date')

  def get_current_timestamp(self):
    now = datetime.datetime.now()
    then = datetime.datetime(1970, 1, 1)
    return int((now - then).total_seconds())
