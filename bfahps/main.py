# -*- coding: utf-8 -*-
#
# Main function
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
from random import seed, randint
from flask import render_template, redirect, request
from bfahps import application
from bfahps.config import *
from bfahps import db
from bfahps.database import User, SaveGame, HighScores, PhotoAlbums
from bfahps.house import launch_game, logout, registration, authentication, services

logger = logging.getLogger(__name__)
db.create_all()

# ---------

def debug(req):
    # debug
    if req.cookies:
        logger.debug('cookies: %s', req.cookies.to_dict())
    if req.form:
        logger.debug('form: %s', req.form.to_dict())
    if req.args:
        logger.debug('args: %s', req.args.to_dict())


@application.route("/")
def house():
    # default page
    debug(request)
    return redirect('/house/home.jsp?startPoint=animation&useBuffer=true')


@application.route("/house/home.jsp", methods=['GET'])
def home():
    # home page
    debug(request)

    use_buffer = request.args.get('useBuffer')
    registered = request.cookies.to_dict('CartoonNetworkBFAHPreg')
    if registered == 'true':
        start_point = request.args.get('startPoint')
    else:
        start_point = 'login'

    return render_template('home.html', startPoint=start_point, userBuffer=use_buffer)


@application.route("/house/Game", methods=['GET','POST'])
def game():
    # Return Game HTML
    debug(request)

    return render_template('game.html', version='1.14.3')


@application.route("/house/Registration", methods=['GET','POST'])
def housereg():
    # Player registartion function
    debug(request)

    if request.method == 'POST':
        posted_values = request.form.to_dict()

        status = registration.do_registration(posted_values)

        if status == '0':
            responce = launch_game(posted_values['username'])
        else:
            responce = "<registration><message username=\"" + posted_values['username'] + "\">"
            seed(posted_values['username'])
            for _ in range(3):
                responce += "<altname name=\"" + posted_values['username'] + str(randint(0, 999)) + "\" reservationId=\"0\" />"
            responce += "</message>"
            for code in status:
                responce += "<message><status code=\"" + str(code) + "\" /></message>"
            responce += "</registration>"

        logger.debug('responce: %s', responce)
        return responce

    # something has gone very wrong if we get to this point.
    return "<status code=\"1\" message=\"\" />"


@application.route("/house/Login", methods=['GET','POST'])
def login():
    # Player Login function
    debug(request)

    if request.method == 'GET':
        action = request.args.get('action')
        if action == 'logout':
            responce = logout()
        else:
            responce = "<status code=\"1\" message=\"\" />"
        logger.debug('responce: %s', responce)
        return responce

    if request.method == 'POST':
        posted_values = request.form.to_dict()

        status,message = authentication.do_login(posted_values)

        if status == 0 and not message:
            responce = launch_game(posted_values['username'])
        else:
            responce = "<status code=\""+str(status)+"\" message=\""+str(message)+"\" />"

        logger.debug('responce: %s', responce)
        return responce

    # something has gone very wrong if we get to this point.
    return "<status code=\"1\" message=\"\" />"


@application.route("/house/Service", methods=['GET','POST'])
def service():
    # Main Game function
    debug(request)

    if request.method == 'POST':
        posted_values = request.form.to_dict()
        cookies = request.cookies.to_dict()

        status,payload = services.do_service(cookies['login'],posted_values)

        if payload:
            responce = str(SAVE_VERSION)+","+str(status)+","+payload
        else:
            responce = str(SAVE_VERSION)+","+str(status)

        logger.debug('responce: %s', responce)
        return responce

    # something has gone very wrong if we get to this point.
    return "<status code=\"1\" message=\"\" />"
