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

"""This module contains the bot starter point ."""

from Core import Bot
import configparser
import logging



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    logging.basicConfig(filename=config['LOG']['filename'], filemode='a', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('Start MOTUX Bot.')
    bot = Bot.Motux(config)
    bot.run()

