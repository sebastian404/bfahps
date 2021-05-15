# -*- coding: utf-8 -*-
#
# Main emulator stub
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
__title__ = 'bfahps'
__version__ = '0.23'
__author__ = 'Sebastian Robinson <Sebastian Robinson>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2006-2021 Sebastian Robinson'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__,
                    static_url_path='',
                    static_folder='../htdocs',
                    template_folder='./templates'
                    )

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bfahp.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

from bfahps import main