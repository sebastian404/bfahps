# -*- coding: utf-8 -*-
#
# Database models
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

from bfahps import db

# Store players login information.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    avatarcode = db.Column(db.String(6), nullable=False)
    goodstanding = db.Column(db.Boolean, nullable=False, default=True)
    hintQuestion = db.Column(db.String(40), nullable=False)
    hintAnswer = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    bdate = db.Column(db.Integer, nullable=False)
    bmonth = db.Column(db.Integer, nullable=False)
    lastseen = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.avatarcode}'')"


# Store players highscores.
class HighScores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    minigame = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    friend = db.Column(db.Integer, nullable=False, default=0)
    score = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"HighScores('{self.minigame}', '{self.mode}')"


# Store players Photo Albums.
class PhotoAlbums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    AlbumID = db.Column(db.Integer, nullable=False)
    PhotosList = db.Column(db.String(100), nullable=False, default='0'*100)

    def __repr__(self):
        return f"PhotoAlbums('{self.AlbumID}')"

# Store Players SaveGame.
class SaveGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    AvatarChosen = db.Column(db.Integer, nullable=False, default=0)
    AvatarName = db.Column(db.String(20), nullable=False, default='[unset]')
    AvatarType = db.Column(db.Integer, nullable=False, default=0)
    AvatarAttrib1 = db.Column(db.Integer, nullable=False, default=0)
    AvatarAttrib2 = db.Column(db.Integer, nullable=False, default=0)
    AvatarAttrib3 = db.Column(db.Integer, nullable=False, default=0)
    AvatarColor1 = db.Column(db.Integer, nullable=False, default=0)
    AvatarColor2 = db.Column(db.Integer, nullable=False, default=0)
    AvatarColor3 = db.Column(db.Integer, nullable=False, default=0)
    AvatarHat = db.Column(db.Integer, nullable=False, default=0)
    AvatarBuddy = db.Column(db.Integer, nullable=False, default=0)
    AvatarCostume = db.Column(db.Integer, nullable=False, default=0)
    AvatarTransport = db.Column(db.Integer, nullable=False, default=0)
    HudCitizenship = db.Column(db.Integer, nullable=False, default=0)
    HudFriendship = db.Column(db.String(4), nullable=False, default='0'*4)
    HudPopularity = db.Column(db.Integer, nullable=False, default=0)
    Duty1Type = db.Column(db.Integer, nullable=False, default=0)
    Duty1Value = db.Column(db.Integer, nullable=False, default=0)
    Duty1Total = db.Column(db.Integer, nullable=False, default=0)
    Duty2Type = db.Column(db.Integer, nullable=False, default=0)
    Duty2Value = db.Column(db.Integer, nullable=False, default=0)
    Duty2Total = db.Column(db.Integer, nullable=False, default=0)
    Duty3Type = db.Column(db.Integer, nullable=False, default=0)
    Duty3Value = db.Column(db.Integer, nullable=False, default=0)
    Duty3Total = db.Column(db.Integer, nullable=False, default=0)
    FavorDone = db.Column(db.Integer, nullable=False, default=0)
    FavorLastType = db.Column(db.Integer, nullable=False, default=0)
    FavorWilt = db.Column(db.Integer, nullable=False, default=0)
    FavorEduardo = db.Column(db.Integer, nullable=False, default=0)
    FavorFrankie = db.Column(db.Integer, nullable=False, default=0)
    FavorMac = db.Column(db.Integer, nullable=False, default=0)
    FavorType = db.Column(db.Integer, nullable=False, default=0)
    FavorStep = db.Column(db.Integer, nullable=False, default=0)
    FavorChar = db.Column(db.Integer, nullable=False, default=0)
    FavorRecip = db.Column(db.Integer, nullable=False, default=0)
    FavorObject = db.Column(db.Integer, nullable=False, default=0)
    AdventuresList = db.Column(db.String(150), nullable=False, default='0'*149)
    AdventureType = db.Column(db.Integer, nullable=False, default=0)
    AdventureStep = db.Column(db.Integer, nullable=False, default=0)
    AdventureDate = db.Column(db.String(8), nullable=False, default='[unset]')
    MinigamesList = db.Column(db.String(100), nullable=False, default='0'*99)
    FurnitureList = db.Column(db.String(350), nullable=False, default='0'*349)
    BirthdayHat = db.Column(db.Integer, nullable=False, default=0)
    NewBirthdayHat = db.Column(db.Integer, nullable=False, default=0)
    MusicTrack = db.Column(db.Integer, nullable=False, default=0)
    AvatarRoom = db.Column(db.Integer, nullable=False, default=0)
    CodesList = db.Column(db.String(100), nullable=False, default='0'*99)
    ObjectsList = db.Column(db.String(100), nullable=False, default='0'*99)
    MyBestFriendPhotoList = db.Column(db.String(100), nullable=False, default='0'*99)
    ToysList = db.Column(db.String(100), nullable=False, default='0'*99)
    Bus = db.Column(db.Integer, nullable=False, default=0)
    BestFriendCode = db.Column(db.String(6), nullable=False, default='0'*6)

    def __repr__(self):
        return f"SaveGame('{self.AvatarChosen}')"
