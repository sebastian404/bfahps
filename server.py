#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Fosters Big Fat Awesome House Party server simulator
#
# Copyright (C) 2006-2021 Sebastian Robinson <sebastian.robinson@podtwo.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

import logging
from bfahps import application

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
    )

    application.run()
