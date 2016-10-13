#!/usr/bin/env python
#
# Provides a the LinuxDayMottola Telegram Bot
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

"""This module contains the Motux class."""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler, Job
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from Hooks import Facebook
import sys
import importlib
import logging

class Motux:

    __config = None

    __updater = None

    __dispatcher = None

    __job_queue = None

    __hooks = {}

    def __init__(self, config):
        """

        :param config:
        """
        self.__config = config
        active_hooks = self.__config['BOT']['hooks'].split(',')
        for hook in active_hooks:
            try:
                hook_module = getattr(sys.modules['Hooks'], hook)
                hook_class = getattr(hook_module, hook)
                self.__hooks[hook] = {
                    'hook': hook_class(self.__config),
                    'timer': 60.0 * 60
                }
            except AttributeError as e:
                print('Error: An error occurred while instance of %s module' % (hook))
                print('=====> %s' % (e))
                exit(2)


    def executer(self, bot, update):
        """

        :param bot:
        :param update:
        :return:
        """
        bot.sendMessage(chat_id=self.__config['CHANNEL']['id'], text="I'm a bot, please talk to me!")

    def error(self, bot, update, error):
        """

        :param bot:
        :param update:
        :return:
        """
        try:
            raise error
        except Unauthorized:
            # remove update.message.chat_id from conversation list
            pass
        except BadRequest:
            # handle malformed requests - read more below!
            pass
        except TimedOut:
            # handle slow connection problems
            pass
        except NetworkError:
            # handle other connection problems
            pass
        except ChatMigrated as e:
            # the chat_id of a group has changed, use e.new_chat_id instead
            pass
        except TelegramError:
            # handle all other telegram related errors
            pass

    def run(self):
        """

        :return: None
        """

        self.__updater = Updater(token=self.__config['KEYS']['bot_api'])
        self.__dispatcher = self.__updater.dispatcher

        executeHandler = MessageHandler([Filters.text], self.executer)
        self.__dispatcher.add_handler(executeHandler)

        self.__dispatcher.add_error_handler(self.error)

        # Define Job Queue
        self.__job_queue = self.__updater.job_queue
        for key, hook in self.__hooks.items():
            self.__job_queue.put(Job(hook.get('hook').job, hook.get('timer'), True), next_t=0.0)


        # Start the Motux Bot
        self.__updater.start_polling(poll_interval=0.1, timeout=10, network_delay=5, clean=False)

        # Run the Motux Bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        self.__updater.idle()

