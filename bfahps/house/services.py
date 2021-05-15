# -*- coding: utf-8 -*-
#
# Replicate /house/Service
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
from bfahps import db
from bfahps.config import *
from bfahps.database import User, SaveGame, HighScores, PhotoAlbums

logger = logging.getLogger(__name__)

def do_service(username, values):
    """
    This function provides the Dynamic services functionality required by the
    Game.

    Called by the Shockwave movie as a HTTP POST request.

    EventCode is a 3 character string that determines which sub function the game is calling.
    """
    logger.info('values: %s', values)

    def SendDutiesServer(values):
        """
        This function updates the Duty variables in the player's savegame.

        Called as player progresses or completes assigned Duties.

        DutyType is an integer representing the type of Duty.
        DutyTotal is an integer representing how many tasks the Duty consists of.
        DutyValue is an integer representing how many tasks the player has left to complete.

        HudUpdate is an integer representing if the Hub variables should be updatd, this is
        set to 1 as duties are completed.
        """
        if values['HudUpdate'] == '1':
            setattr(save, 'HudCitizenship', values['HudCitizenship'])
            setattr(save, 'HudFriendship', values['HudFriendship'])

        for key in values:
            if key.startswith('Duty'):
                setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendFavorsServer(values):
        """
        This function updates the Favours variables in the player's savegame.

        Called as player starts and progresses on Favours.

        FavorWilt, FavorEduardo, FavorFrankie & FavorMac are intergers representing
        the number of favors completed for each character.
        HudUpdate is an integer representing if the Hub variables should be updated, this is
        set to 1 as favours are completed.
        HudFriendship is a 4 character string, consiting of 0 or 4, 1 to 4 representing
        each charactor a favour is owed to.
        """
        if values['HudUpdate'] == '1':
            setattr(save, 'HudFriendship', values['HudFriendship'])
            setattr(save, 'HudPopularity', values['HudPopularity'])

        for key in values:
            if key.startswith('Favor'):
                setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendAdventuresServer(values):
        """
        This function updates the Avdenture variables in the player's savegame.

        Called as player starts and progresses on an Adventure.

        AdventuresList is a 100 character string, consiting of 0 or 1 to represent
        completed adventures.
        """
        if values['HudUpdate'] == '1':
            setattr(save, 'HudCitizenship', values['HudCitizenship'])
            setattr(save, 'HudPopularity', values['HudPopularity'])

        if values['AdventuresListUpdate'] == '1':
            for key in values:
                if key.startswith('Adventure'):
                    setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendAvatarServer(values):
        """
        This function updates the Avatar variables in the player's savegame.

        Called as player creates or edits thier Avatar.
        """
        for key in values:
            if key.startswith('Avatar'):
                setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendAccessoriesServer(values):
        """
        This function updates the Avatar Accessories variables in the player's savegame.

        Called as player selects hats, outfits and other Avatar Accessories.
        """
        for key in values:
            if key.startswith('Avatar'):
                setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendBuddyServer(values):
        """
        This function updates the Avatar Buddy variables in the player's savegame.

        Called as player selects an Avatar Buddy.
        """
        for key in values:
            if key.startswith('Avatar'):
                setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendMiniGameServer(values):
        """
        This function updates the MinigamesList variable in the player's savegame.

        Called as player unlocks Minigames.

        MinigamesList is a 100 character string, consiting of value between 0 to 3,
        0 represnets the Minigame is not unlocked, and 1 to 3 for the dificutly level
        """
        if {'MinigamesList','HudPopularity'}.issubset(values):
            setattr(save, 'MinigamesList', values['MinigamesList'])
            setattr(save, 'HudPopularity', values['HudPopularity'])

        db.session.commit()
        return 0,""


    def SendMiniGameScoreServer(values):
        """
        This function updates the players Personal Highscores for selected Minigame.

        Called after at the end of every Minigame.

        PersonalMinigame is an interger, containg the number of the Minigame selected.
        PersonalMode is an interger, representing the dificulty level of the Minigame.
        """
        if values['PersonalHighscoreUpdate'] == '1':
            for rank in range(1,10+1):
                highscore = HighScores.query.filter_by(userid=user.id, minigame=values['PersonalMinigame'], mode=values['PersonalMode'], rank=rank).first()
                setattr(highscore, 'friend', values['PersonalFriend'+str(rank)])
                setattr(highscore, 'score', values['PersonalScore'+str(rank)])
                db.session.commit()

        db.session.commit()
        return 0,""


    def LogOut(values):
        """
        This function logs the player out of the game.

        Called after the idle timeout has been reached.

        Called with no arguments.
        """
        setattr(user, 'lastseen', datetime.today().strftime('%Y%m%d'))

        db.session.commit()
        return 0,""


    def LogOutTime(values):
        """
        This function confirms the user is still authenticated.

        Called every 30 seconds.

        Called with no arguments.
        """
        setattr(user, 'lastseen', datetime.today().strftime('%Y%m%d'))

        db.session.commit()
        return 0,""


    def SendAlbum(values):
        """
        This function updates the PhotosList variables in the player's Photo Albums.

        Called as the player adds photos into thier Photo Albums.

        PhotosList is a 100 character string, consiting of 0 or 1 to represent unlocked
        Photos.
        AlbumID is an interger, containg the number of the Photo Album selected.
        """
        photoalbum = PhotoAlbums.query.filter_by(userid=user.id, AlbumID=values['AlbumID']).first()
        setattr(photoalbum, 'PhotosList', values['PhotosList'])

        db.session.commit()
        return 0,""


    def SendFurnitureServer(values):
        """
        This function updates the FurnitureList in the player's savegame.

        Called as the player unlocks various items of furniture during the course of Gameplay.

        FurnitureList is a 350 character string, consiting of 0 or 1 to represent unlocked
        items.
        """
        setattr(save, 'FurnitureList', values['FurnitureList'])

        db.session.commit()
        return 0,""


    def SendInitialServer(values):
        """
        This function sets variables in the player's savegame.

        Called once when player first logs into the game, sets all savegame variables to
        an inital state.
        """
        del values['EventCode']
        for key in values:
            setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendTrackerMiniGame(values):
        """
        This function is a tracker used for debugging.

        Called when user plays a Minigame.

        Minigame is an interger, containg the number of the Minigame selected.
        Mode is an interger, representing the dificulty level of the Minigame.
        """
        logger.info('Minigame,Mode: %s', values['Minigame']+','+values['Mode'])

        return 0,""


    def SendHatBornServer(values):
        """
        This function sets the BirthdayHat variables in the player's savegame.

        Called if player logs in on the day and month the player set during Registration.

        Two Hats are unlockable depending when during the games life the players birthday
        occured.

        BirthdayHat is an integer representing the unlocked state of the hat.
        NewBirthdayHat is an integer representing the unlocked state of the hat.
        """
        if {'BirthdayHat','NewBirthdayHat'}.issubset(values):
            setattr(save, 'BirthdayHat', values['BirthdayHat'])
            setattr(save, 'NewBirthdayHat', values['NewBirthdayHat'])

        if {'HudPopularity'}.issubset(values):
            setattr(save, 'HudPopularity', values['HudPopularity'])

        db.session.commit()
        return 0,""


    def SendMusicTrackServer(values):
        """
        This function sets the MusicTrack variables in the player's savegame.

        Called as player selects different music tracks in Notey.

        MusicTrack is an interger, containg the number of the track currently selected,
        or 99 if no track is selected.
        """
        save.MusicTrack = values['MusicTrack']

        db.session.commit()
        return 0,""


    def SendDutiesLoginServer(values):
        """
        This function sets the Duty variables in the player's savegame.

        Called at login to create new duties for the player.

        DutyType is an integer representing the type of Duty.
        DutyTotal is an integer representing how many tasks the Duty consists of.
        DutyValue is an integer representing how many tasks the player has left to complete.
        """
        if values['DutiesUpdate'] == '1':
            for key in values:
                if key.startswith('Duty'):
                    setattr(save, key, values[key])

        db.session.commit()
        return 0,""


    def SendAvatarRoom(values):
        """
        This function sets the AvatarRoom variable in the player's savegame.

        When called enables or disables access to the the Avatar's room in the Mansion.

        AvatarRoom is an interger, containg 0 or 1 to represent if the Avatar's Room in
        Mansion is accessable or not.
        """
        setattr(save, 'AvatarRoom', values['AvatarRoom'])

        db.session.commit()
        return 0,""


    def SendCodesList(values):
        """
        This function updates the CodesList variable in the player's savegame.

        Called when player enters a valid Secret Code into Notey.

        CodesList is a 100 character string, consiting of 0 or 1 to represent
        unlocked items.
        """
        setattr(save, 'CodesList', values['CodesList'])

        db.session.commit()
        return 0,""


    def SendObjectsList(values):
        """
        This function updates the ObjectsList variable in the player's savegame.

        Called when player uses tickets in the Prize Hive in the Shopping Mall.

        ObjectsList is a 100 character string, consiting of 0 or 1 to represent
        unlocked items.
        """
        setattr(save, 'ObjectsList', values['ObjectsList'])

        db.session.commit()
        return 0,""


    def SendMyBestFriendPhotoList(values):
        """
        This function updates the MyBestFriendPhotoList variable in the player's savegame.

        Called when player unlocks a Photo in the Best Friend Photo Album.

        MyBestFriendPhotoList is a 100 character string, consiting of 0 or 1 to represent
        unlocked items.
        """
        setattr(save, 'MyBestFriendPhotoList', values['MyBestFriendPhotoList'])

        db.session.commit()
        return 0,""


    def SendToysList(values):
        """
        This function updates the ToysList variable in the player's savegame.

        Called when player unlocks a Toy from the Toy Chest in Mac's room.

        ToysList is a 100 character string, consiting of 0 or 1 to represent
        unlocked items.
        """
        if {'ToysList'}.issubset(values):
            setattr(save, 'ToysList', values['ToysList'])

        if {'HudPopularity'}.issubset(values):
            setattr(save, 'HudPopularity', values['HudPopularity'])

        db.session.commit()
        return 0,""


    def SendTrackerToy(values):
        """
        This function is a tracker, used for debugging.

        Called when player interacts with a Toy in the Toy Chest in Mac's room.

        Toys is an interger, containg the number of the Toy selected.
        """
        logger.info('toy: %s', values['Toys'])

        return 0,""


    def SendSendBus(values):
        """
        This function sets the Bus variable in the player's savegame.

        When called enables or disables the Foster's bus to apear outside the house, the bus
        enables players to visit locations around town.

        Bus is a interger, containg 0 or 1 to represent if the Bus is unlocked.
        """
        setattr(save, 'Bus', values['Bus'])

        db.session.commit()
        return 0,""


    def GetMiniGameServer(values):
        """
        This function provides highscores for selected Minigame.

        The function will reurn the highscore of each gamemode of the players BestFriend if
        set, followed by the players 10 highscores for each dificulty level, and the world
        highscores for each game dificulty level.

        Minigame is an interger, containg the number of the Minigame selected.
        """
        ret=[]

        if SAVE_VERSION >= 140:
            bestfriendcode = save.BestFriendCode
            bestfrienduser = User.query.filter_by(avatarcode=bestfriendcode).first()

            if bestfrienduser:
                for mode in range(1,3+1):
                    highscore = HighScores.query.filter_by(userid=bestfrienduser.id, minigame=values['Minigame'], mode=mode, friend=0).first()
                    if highscore:
                        ret.append(highscore.score)
                    else:
                        ret.append(0)
            else:
                ret.extend([0,0,0])
        else:
            ret.extend([0,0,0])

        for mode in range(1,3+1):
            highscore = HighScores.query.filter_by(userid=user.id, minigame=values['Minigame'], mode=mode).order_by(HighScores.rank).all()
            for rank in range(0,10):
                ret.append(highscore[rank].friend)
            for rank in range(0,10):
                ret.append(highscore[rank].score)

        ret.extend(["player1","player2","player3","player4","player5","player6","player7","player8","player9","player10","0","0","0","0","0","0","0","0","0","0"])
        ret.extend(["player1","player2","player3","player4","player5","player6","player7","player8","player9","player10","0","0","0","0","0","0","0","0","0","0"])
        ret.extend(["player1","player2","player3","player4","player5","player6","player7","player8","player9","player10","0","0","0","0","0","0","0","0","0","0"])

        ret.append(0)
        retstr=','.join(str(value) for value in ret)

        return 0,retstr


    def ValidateName(values):
        """
        This function validates the player provided Avatar Name.

        The orignal would additioanly check for offensive/inappropriate
        words, this has not been implmented here.

        AvatarName is a 20 character string, provided by player.
        """
        if set('[~!@#$%^&*()_+{}":;\']+$').intersection(values['AvatarName']):
            return 1,""

        return 0,""


    def GetFirstTimeState(values):
        """
        This function returns the current players savegame.

        The function is only called once during preloading.
        """
        ret=[]

        ret.append((datetime.today()-datetime.strptime(user.lastseen,'%Y%m%d')).days)
        ret.append(datetime.today().strftime('%Y%m%d'))
        ret.append(IDLE_TIMEOUT)
        ret.append("2000"+str(user.bmonth).zfill(2)+str(user.bdate).zfill(2))
        ret.append(user.avatarcode)

        ret.append(save.AvatarChosen)
        ret.append(save.AvatarType)
        ret.append(save.AvatarName)
        ret.append(save.AvatarAttrib1)
        ret.append(save.AvatarAttrib2)
        ret.append(save.AvatarAttrib3)
        ret.append(save.AvatarColor1)
        ret.append(save.AvatarColor2)
        ret.append(save.AvatarColor3)
        ret.append(save.AvatarHat)
        ret.append(save.AvatarBuddy)
        ret.append(save.AvatarCostume)
        ret.append(save.AvatarTransport)
        ret.append(save.HudCitizenship)
        ret.append(save.HudFriendship)
        ret.append(save.HudPopularity)

        ret.append(save.Duty1Type)
        ret.append(save.Duty1Value)
        ret.append(save.Duty1Total)
        ret.append(save.Duty2Type)
        ret.append(save.Duty2Value)
        ret.append(save.Duty2Total)
        ret.append(save.Duty3Type)
        ret.append(save.Duty3Value)
        ret.append(save.Duty3Total)

        ret.append(save.FavorDone)
        ret.append(save.FavorLastType)
        ret.append(save.FavorWilt)
        ret.append(save.FavorEduardo)
        ret.append(save.FavorFrankie)
        ret.append(save.FavorMac)
        ret.append(save.FavorType)
        ret.append(save.FavorStep)
        ret.append(save.FavorChar)
        ret.append(save.FavorRecip)
        ret.append(save.FavorObject)

        ret.append(save.AdventuresList)
        ret.append(save.AdventureType)
        ret.append(save.AdventureStep)
        ret.append(save.AdventureDate)

        ret.append(save.MinigamesList)
        for minigame in range(1,MAX_MINIGAME+1):
            for mode in range(1,3+1):
                highscore = HighScores.query.filter_by(userid=user.id, minigame=minigame, mode=mode, friend=0).first()
                if highscore:
                    ret.append(highscore.score)
                else:
                    ret.append(0)
        for albumid in range(1,MAX_ALBUM+1):
            photoalbum = PhotoAlbums.query.filter_by(userid=user.id, AlbumID=albumid).first()
            ret.append(photoalbum.PhotosList)
        ret.append(save.FurnitureList)
        ret.append(save.BirthdayHat)
        ret.append(save.NewBirthdayHat)
        ret.append(save.MusicTrack)
        ret.append(save.AvatarRoom)
        ret.append(save.CodesList)
        ret.append(save.ObjectsList)
        ret.append(save.MyBestFriendPhotoList)
        ret.append(save.ToysList)
        ret.append(save.Bus)
        ret.append(save.BestFriendCode)
        bestfrienduser = User.query.filter_by(avatarcode=save.BestFriendCode).first()
        if bestfrienduser:
            bestfriendsave = SaveGame.query.filter_by(userid=user.id).first()
            ret.append(bestfriendsave.AvatarType)
            ret.append(bestfriendsave.AvatarName)
            ret.append(bestfriendsave.AvatarAttrib1)
            ret.append(bestfriendsave.AvatarAttrib2)
            ret.append(bestfriendsave.AvatarAttrib3)
            ret.append(bestfriendsave.AvatarColor1)
            ret.append(bestfriendsave.AvatarColor2)
            ret.append(bestfriendsave.AvatarColor3)
            ret.append(bestfriendsave.AvatarHat)
            ret.append(bestfriendsave.AvatarBuddy)
            ret.append(bestfriendsave.AvatarCostume)
            ret.append(bestfriendsave.AvatarTransport)
        else:
            ret.extend([0,"[unset]",0,0,0,0,0,0,0,0,0,0])
        retstr=','.join(str(value) for value in ret)
        return 0,retstr


    def ValidateBestFriendAvatarCode(values):
        """
        This function validates the user provided Best Friend Code, and returns Avatar
        attributes if valid.

        The function will in addition will unset BestFriend if provided code is '000000'.

        BestFriendCode is a 6 character string, provided by player.
        """
        if values['BestFriendCode'] == '000000':
            setattr(save, 'BestFriendCode', '000000')
            db.session.commit()

            return 0,"000000,0,[unset],0,0,0,0,0,0,0,0,0,0"

        bestfrienduser = User.query.filter_by(avatarcode=values['BestFriendCode']).first()
        if bestfrienduser:
            setattr(save, 'BestFriendCode', values['BestFriendCode'])
            db.session.commit()

            bestfriendsave = SaveGame.query.filter_by(userid=bestfrienduser.id).first()
            ret=[]
            ret.append(bestfrienduser.avatarcode)
            ret.append(bestfriendsave.AvatarType)
            ret.append(bestfriendsave.AvatarName)
            ret.append(bestfriendsave.AvatarAttrib1)
            ret.append(bestfriendsave.AvatarAttrib2)
            ret.append(bestfriendsave.AvatarAttrib3)
            ret.append(bestfriendsave.AvatarColor1)
            ret.append(bestfriendsave.AvatarColor2)
            ret.append(bestfriendsave.AvatarColor3)
            ret.append(bestfriendsave.AvatarHat)
            ret.append(bestfriendsave.AvatarBuddy)
            ret.append(bestfriendsave.AvatarCostume)
            ret.append(bestfriendsave.AvatarTransport)
            retstr=','.join(str(value) for value in ret)
            return 0,retstr

        return 1,""


    # Validate posted variables
    event_code = values['EventCode']
    if event_code:
        user = User.query.filter_by(username=username).first()

        if not user:
            return 1,""

        # Get players savegame.
        save = SaveGame.query.filter_by(userid=user.id).first()

        # Send Events.
        if event_code == '001':
            return SendDutiesServer(values)

        if event_code == '002':
            return SendFavorsServer(values)

        if event_code == '003':
            return SendAdventuresServer(values)

        if event_code == '004':
            return SendAvatarServer(values)

        if event_code == '005':
            return SendAccessoriesServer(values)

        if event_code == '006':
            return SendBuddyServer(values)

        if event_code == '007':
            return SendMiniGameServer(values)

        if event_code == '008':
            return SendMiniGameScoreServer(values)

        if event_code == '009':
            return LogOut(values)

        if event_code == '010':
            return LogOutTime(values)

        if event_code == '011':
            return SendAlbum(values)

        if event_code == '012':
            return SendFurnitureServer(values)

        if event_code == '013':
            return SendInitialServer(values)

        if event_code == '014':
            return SendTrackerMiniGame(values)

        if event_code == '015':
            return SendHatBornServer(values)

        if event_code == '016':
            return SendMusicTrackServer(values)

        if event_code == '017':
            return SendDutiesLoginServer(values)

        if event_code == '018':
            return SendAvatarRoom(values)

        if event_code == '019':
            return SendCodesList(values)

        if event_code == '020':
            return SendObjectsList(values)

        if event_code == '021':
            return SendMyBestFriendPhotoList(values)

        if event_code == '022':
            return SendToysList(values)

        if event_code == '023':
            return SendTrackerToy(values)

        if event_code == '024':
            return SendSendBus(values)

        # Get Events.
        if event_code == '101':
            return GetMiniGameServer(values)

        if event_code == '102':
            return ValidateName(values)

        if event_code == '103':
            return GetFirstTimeState(values)

        if event_code == '104':
            return ValidateBestFriendAvatarCode(values)

    # something has gone very wrong if we get to this point.
    return 1,""
