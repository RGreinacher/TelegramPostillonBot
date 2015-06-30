#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

# DataManger for handling a SQLite DB for log reasons and for keeping
# track of which user got which newsticker
# to serve every newsticker to every user.
# Copyright (c) 2015 Robert Greinacher, development@robert-greinacher.de



import sqlite3
import os
import datetime



# defining constants and globals:
BE_VERBOSE = True
SQLITE_FILENAME = os.getcwd() + '/botDB.sqlite'
ALLOW_CLEAR_DB = True



class DataManager:
  def __init__(self):
    self.dbConnection = sqlite3.connect(SQLITE_FILENAME)
    self.dbCursor = self.dbConnection.cursor()

    if not self.required_tables_are_present():
      if BE_VERBOSE: print('required tables are not present; creating...')
      self.create_required_tables()

  def cleanup(self):
    self.dbCursor.close()
    self.dbConnection.close()

# PRAGMA MARK: - setter

  def new_message(self, message_object):
    if (
      not self.isset(message_object, 'message_id') or
      not self.isset(message_object, 'chat') or
      not self.isset(message_object['chat'], 'id') or
      not self.isset(message_object, 'text')
    ):
      return False

    query = 'SELECT id FROM message WHERE id = ?'
    self.dbCursor.execute(query, (message_object['message_id'],))

    if not self.data_set_exists():
      # save the chat of the request
      self.new_chat(message_object['chat'])

      # insert new message object
      query = 'INSERT INTO message VALUES(?, ?, ?, ?)'
      self.dbCursor.execute(
        query, (message_object['message_id'],
          message_object['chat']['id'],
          message_object['text'],
          self.get_current_timestamp()
        ))
      self.dbConnection.commit()

  def new_chat(self, user_or_group_object):
    if (
      not self.isset(user_or_group_object, 'id') or
      not (
        self.isset(user_or_group_object, 'title') or
        self.isset(user_or_group_object, 'first_name')
      )
    ):
      return False

    query = 'SELECT * FROM chat WHERE id = ?'
    self.dbCursor.execute(query, (user_or_group_object['id'],))

    if not self.data_set_exists():
      query = 'INSERT INTO chat VALUES(?, ?, ?)'
      name = ''

      # groups and single user chats differ in the name
      if 'title' in user_or_group_object:
        name = user_or_group_object['title']
      else:
        name = user_or_group_object['first_name']

      self.dbCursor.execute(
        query, (user_or_group_object['id'], name, self.get_current_timestamp())
      )
      self.dbConnection.commit()

  def new_newsticker(self, array_of_newsticker):
    for ticker in array_of_newsticker:
      query = 'SELECT id FROM newsticker WHERE newsticker = ?'
      self.dbCursor.execute(query, (ticker,))

      if not self.data_set_exists():
        query = 'INSERT INTO newsticker (newsticker, created_at) \
          VALUES(?, ?)'
        self.dbCursor.execute(query, (ticker, self.get_current_timestamp()))
        self.dbConnection.commit()

# PRAGMA MARK: - getter

  def get_newsticker_for_chat(self, chat_id):
    query = 'SELECT id, newsticker \
      FROM newsticker \
      LEFT JOIN (SELECT newsticker_id, COUNT(*) AS "count" \
      FROM newsticker_chat \
      WHERE chat_id = ? \
      GROUP BY newsticker_id) ON id = newsticker_id \
      ORDER BY count ASC, created_at DESC \
      LIMIT 0, 1'
    self.dbCursor.execute(query, (chat_id,))

    try:
      newsticker_id, newsticker = self.dbCursor.fetchone()
      self.combine_newsticker_with_chat(newsticker_id, chat_id)
      return newsticker
    except 'NoneType' as e:
      if BE_VERBOSE: print('error fetching newsticker from DB')
      return '++++ Kabott gegangen: Postillon bot weiß nicht weiter ++++'

  def get_stistic(self):
    self.dbCursor.execute('SELECT COUNT(*) FROM chat')
    chat_count = self.dbCursor.fetchone()[0]

    self.dbCursor.execute('SELECT COUNT(*) FROM newsticker')
    newsticker_count = self.dbCursor.fetchone()[0]

    self.dbCursor.execute('SELECT COUNT(*) FROM newsticker_chat')
    request_count = self.dbCursor.fetchone()[0]

    return chat_count, newsticker_count, request_count

# PRAGMA MARK: - helper

  def combine_newsticker_with_chat(self, newsticker_id, chat_id):
    query = 'INSERT INTO newsticker_chat (newsticker_id, chat_id, created_at) \
      VALUES(?, ?, ?)'
    self.dbCursor.execute(
      query, (newsticker_id, chat_id, self.get_current_timestamp())
    )
    self.dbConnection.commit()

  def required_tables_are_present(self):
    query = 'SELECT name FROM sqlite_master WHERE type="table" AND name=?'
    for table in ['message', 'chat', 'newsticker']:
      self.dbCursor.execute(query, (table,))
      if not self.data_set_exists():
        return False
    return True

  def create_required_tables(self):
    self.dbCursor.execute('create table newsticker \
      (id INTEGER PRIMARY KEY, \
      newsticker TEXT, \
      created_at INTEGER)')

    self.dbCursor.execute('create table chat \
      (id INTEGER PRIMARY KEY, \
      name TEXT, \
      created_at INTEGER)')

    self.dbCursor.execute('create table message \
      (id INTEGER PRIMARY KEY, \
      chat_id INTEGER, \
      text TEXT, \
      created_at INTEGER)')

    self.dbCursor.execute('create table newsticker_chat \
      (id INTEGER PRIMARY KEY, \
      newsticker_id INTEGER, \
      chat_id INTEGER, \
      created_at INTEGER)')

    self.dbConnection.commit()

  def data_set_exists(self):
    for row in self.dbCursor:
      return True
      break
    return False

  def get_current_timestamp(self):
    now = datetime.datetime.now()
    then = datetime.datetime(1970, 1, 1)
    return int((now - then).total_seconds())

  def isset(self, dictionary, key):
    try:
      dictionary[key]
    except (NameError, KeyError) as e:
      return False
    else:
      return True

  def clear_db(self):
    if not ALLOW_CLEAR_DB and BE_VERBOSE:
      print('set the ALLOW_CLEAR_DB flag to True to execute clear_db()')
    elif ALLOW_CLEAR_DB:
      self.dbCursor.execute('DELETE FROM newsticker WHERE 1')
      self.dbCursor.execute('DELETE FROM chat WHERE 1')
      self.dbCursor.execute('DELETE FROM message WHERE 1')
      self.dbCursor.execute('DELETE FROM newsticker_chat WHERE 1')
      self.dbConnection.commit()
