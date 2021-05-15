# -*- coding: utf-8 -*-
#
# Replicate /house/Login
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
from bfahps import db
from bfahps.database import User

logger = logging.getLogger(__name__)

def do_login(values):
    """
    This function provides the Account athentication functionality required by the

    Called by the Shockwave movie as a HTTP POST request.

    TODO
    """
    logger.debug('values: %s', values)

    def forgotpassword(values):
        # Prompt player for Hintquestion and provide password if correct.
        action = values['action']

        if not {'username'}.intersection(values):
            return 100,""

        user = User.query.filter_by(username=values['username']).first()
        if not user:
            return 107,""

        if action:
            if action == 'forgotPassword':
                return 0, str(user.hintQuestion)

            if action == 'forgotPasswordWithHint' and values['answer'] == user.hintAnswer:
                return 0, str(user.password)

            return 108,""

        return 1,""


    def changepassword(values):
        # Rest player password and Hint Question/Answer.
        logger.debug('values: %s', values)

        if not {'username'}.intersection(values):
            return 100,""

        if not {'password'}.intersection(values):
            return 101,""

        user = User.query.filter_by(username=values['username']).first()
        if not user:
            return 107,""

        if set('[~!@#$%^&*()_+{}":;\']+$').intersection(values['newpass']):
            return 110,""

        if values['newpass'] != values['passwordConfirm']:
            return 105,""

        if values['newpass'] == values['oldpass']:
            return 106,""

        if {'username','oldpass','verifypass','newpass','hintQuestion','hintAnswer'}.issubset(values):
            user.password = values['password']
            user.hintQuestion = values['hintQuestion']
            user.hintAnswer = values['hintAnswer']
            db.session.commit()

            return 0,""

        return 1,""

    # Validate posted variables
    if {'action'}.intersection(values):
        action = values['action']
        logger.debug('action: %s', action)
        if action in ('forgotPassword','forgotPasswordWithHint'):
            return forgotpassword(values)
        if action == 'changePassword':
            return changepassword(values)

    if not {'username'}.intersection(values):
        return 100,""

    if not {'password'}.intersection(values):
        return 101,""

    user = User.query.filter_by(username=values['username']).first()
    if not user:
        return 102,""

    if {'password','username'}.issubset(values):
        if values['password'] != user.password:
            return 103,""

        if values['resetPswdStatus'] == 'true':
            return 50,""

        if not user.goodstanding:
            return 104,""

        return 0,""

    # something has gone very wrong if we get to this point.
    return 1,""
