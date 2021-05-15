# -*- coding: utf-8 -*-
#
# Replicate /house/Registration
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
from datetime import datetime
from random import seed, randbytes
from bfahps import db
from bfahps.config import *
from bfahps.database import User, SaveGame, HighScores, PhotoAlbums

logger = logging.getLogger(__name__)

def do_registration(values):
    """
    This function provides the Account registration functionality required by the

    Called by the Shockwave movie as a HTTP POST request.

    TODO
    """
    logger.debug('values: %s', values)

    def create_user(values):
        # Create User, Savegame, Photo Albums and Highsore
        logger.debug('values: %s', values)

        seed(values['username'])
        acode=(randbytes(3).hex()).upper()
        user = User(
            username = values['username'],
            avatarcode = acode,
            password = values['password'],
            hintQuestion = values['hintQuestion'],
            hintAnswer = values['hintAnswer'],
            state = values['state'],
            bdate = values['bdate'],
            bmonth = values['bmonth'],
            lastseen = datetime.today().strftime('%Y%m%d')
            )
        db.session.add(user)
        db.session.commit()

        savegame = SaveGame(
            userid=user.id
            )
        db.session.add(savegame)
        db.session.commit()

        for minigame in range(1,MAX_MINIGAME+1):
            for mode in range(1,3+1):
                for rank in range(1,10+1):
                    highscores = HighScores(
                        userid = user.id,
                        minigame = minigame,
                        mode = mode,
                        rank = rank,
                        friend = 0,
                        score = 0
                    )
                    db.session.add(highscores)
        db.session.commit()

        for albumid in range(1,MAX_ALBUM+1):
            photoalbum = PhotoAlbums(
                userid = user.id,
                AlbumID = albumid,
                PhotosList = '0'*100
            )
            db.session.add(photoalbum)
        db.session.commit()

        return True

    # Validate posted variables
    status = []

    if not {'username'}.intersection(values):
        status.append("200")

    if not {'password'}.intersection(values):
        status.append("201")

    if not {'bdate'}.intersection(values):
        status.append("202")

    if not {'bmonth'}.intersection(values):
        status.append("203")

    if not {'hintQuestion'}.intersection(values):
        status.append("204")

    if not {'hintAnswer'}.intersection(values):
        status.append("205")

    if not {'state'}.intersection(values):
        status.append("206")

    if values['username'] and User.query.filter_by(username=values['username']).first():
        status.append("207")

    if set('[~!@#$%^&*()_+{}":;\']+$').intersection(values['username']):
        status.append("208")

    if set('[~!@#$%^&*()_+{}":;\']+$').intersection(values['password']):
        status.append("209")

    if values['password'] != values['passwordConfirm']:
        status.append("210")

    if not status and {'hintQuestion','bdate','bmonth','state','hintAnswer','passwordConfirm','password','username'}.issubset(values):
        if create_user(values):
            status='0'

    # something has gone very wrong if we get to this point.
    if not status:
        staus='1'

    return status
