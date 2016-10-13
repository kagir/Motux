#!/usr/bin/env python
#
# Provides a the Facebook Hooks
# Copyright (C) 2015-2016
# Girardi Carlo Antonio <kagir.dev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
# -*- coding: utf-8 -*-

"""This module contains the Facebook class."""

import time
import facebook
from pymongo import MongoClient


class Facebook:
    __config = None
    __graph = None
    __profile = None
    __database = None

    def __init__(self, config):
        """
        Class constructor
        :param config:
        """
        self.__config = config
        self.__graph = facebook.GraphAPI(access_token=self.__config['KEYS']['facebook_api'],
                                         version=self.__config['KEYS']['facebook_version'])
        self.__profile = self.__graph.get_object(id=self.__config['FACEBOOK']['profile'])
        client_mongo = MongoClient(self.__config['MONGO']['host'],int(self.__config['MONGO']['port']))
        self.__database = client_mongo[self.__config['MONGO']['database']]


    def posts(self):
        """

        :return: messages
        """
        posts = self.__graph.get_connections(self.__profile['id'], connection_name='posts')
        db_posts = self.__database.motux
        messages = []
        for post in posts['data']:
            if db_posts.find({'id': post['id']}).count() == 0:
                # args = {'fields' : 'picture,full_picture,link,story,likes,attachments,type,icon,status_type,name,updated_time,created_time', }
                args = {'fields': 'picture,full_picture,link,story,type,icon,status_type,name,updated_time,created_time,attachments,message', }
                postData = self.__graph.get_object(post['id'], **args)
                if postData.get('type') == 'event':
                    event_id = postData.get('attachments').get('data')[0].get('target').get('id')
                    event_obj = self.__graph.get_object(id=event_id)
                    postData['event_data'] = event_obj
                #print(postData)
                #db_posts.insert_one(postData)
                messages.append(postData)
        return messages


    def job(self,bot,jobs):
        """

        :param bot:
        :param jobs:
        :return: None
        """
        bot_action = {
            'photo': lambda id, x: bot.sendPhoto(chat_id=id, photo=x.get('full_picture')),
            'event': lambda id, x: bot.sendMessage(chat_id=id, text=x.get('event_data').get('description')),
            'link': lambda id, x: bot.sendMessage(chat_id=id, text=x.get('link')),
            'status': lambda id, x: bot.sendMessage(chat_id=id, text=x.get('message')),
            'nothing': None,
        }
        for message in self.posts():
            bot_action[message.get('type')](id=self.__config['CHANNEL']['id'], x=message)
            time.sleep(1)


