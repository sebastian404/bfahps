# -*- coding: utf-8 -*-
#
# services stub
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

from datetime import datetime
from flask import make_response, redirect

def launch_game(username):
    # Set cookie and redirect to game page
    responce = make_response("<status code=\"0\" message=\"/house/Game?"+str(datetime.now().timestamp()).split('.')[0]+"\" />")
    responce.set_cookie('login', username)
    return responce

def logout():
    # Destroy cookie and redirect to login page
    responce = make_response(redirect('/house/home.jsp?startPoint=login'))
    responce.set_cookie('login', '', expires=0)
    return responce
