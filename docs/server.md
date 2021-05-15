# Big Fat Awesome House Party Server Reverse Engineered
All information in this document was determined by from playing the game and snooping network traffic and later altering returned values to observe the effect on the game.


## Server Architecture
The server was powered by Apache Tomcat serving both static and dynamic content.  Dynamic services were implemented using JavaServer Pages to provide backend services to the game.

Game assets where served from the `i.awesomehouseparty.com` domain, with assets used in the website severed initially from `i.cartoonnetwork.com` and later `i.cdn.turner.com` domains.

Game assets where located under the `/toonahp/` directory, while website assets where located under the `/toon/promos/200604_bfahp/tools/gamesite/` directory.

For a full list of assets see the [files.md](files.md) document.


## Cookies
Four cookies were used throughout the game.

- `JSESSIONID; path="/house"; domain=awesomehouseparty.com; path_spec; discard`
  - Generated by Servlet containers and used for session management in J2EE web applications.
- `ffhpauthid; path="/house"; domain=awesomehouseparty.com; discard`
  - Generated server side once authenticated, used for session management.
- `login; path="/house"; domain=awesomehouseparty.com; discard`
  - Set client side once authenticated, used for session management.
- `CartoonNetworkBFAHPreg; path="/house"; domain=awesomehouseparty.com; expires=+1year`
  - Set client side once authenticated, used by the landing page to skip the introduction on susquent visits. set to expire after 1 year after creation.


## Registration
Registration is a Shockware Flash 8 movie that is the main entry page for the game, it allows players to view Character Bios, view the Privacy Policy, a FAQ for Parents.  More importantly it supplied the functionality to Register an Account, Recovering and Resetting user passwords and Login in to the game.

- located:
  - `/toonahp/registration/registration.swf`
- arguments:
  - `CN_configLoc`
    - URL to an XML files the movie used for configuration,
    - default: `http://i.awesomehouseparty.com/toonahp/registration/config.xml`
  - `CN_loginService`
    - URL to the Dynamic Service for Authentication
    - default: `http://i.awesomehouseparty.com/house/Login`
  - `CN_regService`
    - URL to the Dynamic Service for Registration
    - default: `http://i.awesomehouseparty.com/house/Registration`
  - `CN_startPoint`
    - variable used to determine the frame the movie starts on, `login` skips the intro.
    - default: `animation`
  - `CN_useBuffer`
    - variable used to determine if if Ads should be shown, and if a confirmation page be shown.
    - default: `true`

#### Versions
Five different builds of the registration movie were observed during the games lifetime, these are documented in [versions.md](versions.md)

There was one major change to the movie introduced with build 1.8.1.1 (11 Jan 2007), mainly Cosmetic, the intro movie was removed, the two registration frames were compressed down into one pages.

`config.xml` and SWF assets relocated to:
`/toonahp/registration/tools/`

FLV assets relocated to:
`/toonahp/registration/tools/flv/`

A PNG file was added
`/toonahp/registration/tools/about_popdemand.png`

In addition the `<release_info>` elements where moved from `login.xml` to `config.xml` with the addition to the `<updates>` of elements `month` denoting the month of the update and `swfloc` being the URL to a single frame SWF movie.

#### XML files
Registration requires a config.xml file for it's configuration, mainly linking to other XMLs files for further settings and assets.

##### `config.xml`
The config file provides various settings required for the registration movie.

- located:
  - `/toonahp/registration/config.xml`
- elements
  - `<chars>`
    - Contains elements one for each character bio with two attributes `swloc`  and `flv` that provide the URL for a single frame Flash Movie(SWF) and videos Flash Video(FLV) for each character.
  - `<xml>`
    - Contains three sub-Elements `login`, `faq` and `privacy` that provide URLs for further XML files used inside the movie.

##### `login.xml`
The login XML file contains elements used to populate the 'New Features' tab on the Login page.

- located
  - `/toonahp/registration/login.xml`
- elements
  - `<release_info>`
    - Contains multiple sub-Elements `release` and `text` that provides details on the additional features added in update.
  - `<release>`
    - Contains three attributes `id`, `date` and `active`
    - `id`
      - Incremental integer used to order releases.
    - `date`
      - String relating to the date the additional features was added
    - `active`
      - Integer used to determine if release to be shown.
    - `<text>`
      - Contains Character Data relating to the additional features added in update.

##### `faq.xml`
The faq XML file contains elements used to populate the 'For Parents' Frame available throughout the movie.

- located
  `/toonahp/registration/faq.xml`
- elements
  - `<qa_pair>`
    - Contains multiple `question` and `answer` sub-Elements.
    - `<question>`
      - Used in the 'For Parents' Frame, contains questions.
    - `<answer>`
      - Used in the 'For Parents' Frame, contains answers.

##### `privacy.xml`
The privacy XML file contains elements used to populate the Privacy Policy Frame accessible from the Registration and Login pages.

- located
  - `/toonahp/registration/privacy.xml`
- elements
  - `<privacy>`
    - Contains character data relating to the Privacy Policy.

#### Dynamic Services
There are three Dynamic Services the registration movie depends upon, the movie uses the HTTP POST mechanism to send various variables to the Dynamic Services, return values are either XML or a redirect if authenticated.

##### `/house/Login`
Provides user authentication, including the option to reset and recover passwords.

- arguments:
  - `action`
    - Used to represent the requested action to be carried out, other than login.
  - `forgotPassword`
    - If username is valid will return the Hint Question set during registration.
  - `forgotPasswordWithHint`
    - If Hint Answer is valid will return the players password
  - `changePassword`
    - Updates users password and Hint Answer/Question.
  - `username`
    - Players username entered at Login page.
  - `password`
    - Players password entered at Login page.
  - `resetPswdStatus`
    - If username and Password are value will route to page to allow player to change password and set a new Hint Answer/Question.

  returns:
  XML file with one element `status` containing two attributes `code` and `message`

  - elements
    - `<status>`
      - Contains two attributes.
        - `code`
          -   0 = Player authenticated.
          -   1 = Internal Server error.
          -   2 = Internal Server error.
          -   3 = Internal Server error.
          -  50 = Reset password tickbox selected.
          - 100 = Value 'username' not set.
          - 101 = Value 'password' not set.
          - 102 = Value 'username' is not a valid player.
          - 103 = Value 'password' incorect for player.
          - 104 = Player account has been closed.
          - 105 = Value 'password' incorect for player.
          - 106 = Values 'oldpass' and 'newpass' are the same.
          - 107 = Value 'username' is not a valid player.
          - 108 = Value 'answer' is the Hint Answer provided during registration.
          - 109 = Internal Server error.
          - 110 = Value 'password' contains invalid characters.
        - `message`
          - If status is 0 message will contain the URL to start the game.
          - If forgotPasswordWithHint is called with correct Answer, contains players password.

##### `/house/Registration`
Validates variables submitted by the player from the Registration frame of the movie.

- arguments:
  - `username`,`password`,`passwordConfirm`,`hintQuestion`,`hintAnswer`,`bdate`,`bmonth`,`state`
    - Values entered in registration page.
- returns:
  - XML file with one element `registration` that contains multiple `message` sub-elements
    - elements
      - `<message>`
        - Contains three attributes.
      - `username`
        - Value 'username' provides by player in Registration Screen.
      - `altname`
        - Alternative username suggestions, used when 'username' is already registered account.
      - `code`
        -   0 = Player account created.
        -   1 = Internal Server error.
        -   2 = Internal Server error.
        -   3 = Internal Server error.
        - 200 = Value 'username' not set.
        - 201 = Value 'password' not set.
        - 202 = Value 'bdate' not set.
        - 203 = Value 'bmonth' not set.
        - 204 = Value 'hintQuestion' not set.
        - 205 = Value 'hintAnswer' not set.
        - 206 = Value 'state' not set.
        - 207 = Value 'username' is an existing player.
        - 208 = Value 'username' contains invalid characters.
        - 209 = Value 'password' contains invalid characters.
        - 210 = Value 'password' and 'passwordConfirm' do not match.

##### `/house/Game`
Returns HTML page to launch the game.

- arguments:
  - `userBuffer`
    - If set to true will provide HTML with Adverts, otherwise an alternative layout without Adverts.


## Game
Game is a Shockwave 10 movie that contains the main body of the game itself.

- located:
  - `/toonahp/game/game.dcr`
- arguments:
  - `sw1`
    - Full path to the Dynamic Service for the game.
    - default: `http://i.awesomehouseparty.com/house/Service`
  - `sw2`
    - Version of the game

#### Versions
Fifteen different builds of the movie observed during the games lifetime, these are documented in [versions.md](versions.md)

Most of the versions where content updates adding additional areas, quests, adventures and objects to the game, however some versions where minor updates to resolve bugs/issues.

#### Dynamic Services
There was only one Dynamic Service the game movie depended upon, the movie uses the HTTP POST mechanism to send various variables to the Dynamic Services, return values would be a string of values separated by commas.

Return values where at least 2 values, the first value is the version of the save game, initially this would be 30, but as later versions would increase inline with the game version, the second value is status of the called function, to represent if the called function completed correctly `0`or not `1`.

##### `/house/Service`
This Service provided save game services to the game, providing information pertaining to previous progress and updating current progress.

- arguments:
  - `EventCode`
    - There are 28 different EventCodes values representing a different function, they are split mainly into 'Send' and 'Get' types.
    - `001` SendDutiesServer
      - Updates the Duty variables in the player's save game, Called as player progresses or completes assigned Duties.
        - arguments:
          - `Duty1Type`
          - `Duty1Total`
          - `Duty1Value`
          - `Duty2Type`
          - `Duty2Total`
          - `Duty2Value`
          - `Duty3Type`
          - `Duty3Total`
          - `Duty3Value`
          - `HudUpdate`
          - `HudCitizenship`
          - `HudFriendship`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `002` SendFavorsServer
      - Updates the Favours variables in the player's save game, Called as player starts and progresses on Favours.
        - arguments:
          - `FavorDone`
          - `FavorType`
          - `FavorStep`
          - `FavorChar`
          - `FavorRecip`
          - `FavorObject`
          - `FavorWilt`
          - `FavorEduardo`
          - `FavorFrankie`
          - `FavorMac`
          - `FavorLastType`
          - `HudUpdate`
          - `HudFriendship`
          - `HudPopularity`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `003` SendAdventuresServer
      - Updates the Adventure variables in the player's save game, Called as player starts and progresses on an Adventure.
        - arguments:
          - `AdventuresListUpdate`
          - `AdventuresList`
          - `AdventureType`
          - `AdventureStep`
          - `AdventureDate`
          - `HudUpdate`
          - `HudCitizenship`
          - `HudPopularity`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `004` SendAvatarServer
      - Updates the Avatar variables in the player's save game, Called as player creates or edits their Avatar.
        - arguments:
          - `AvatarChosen`
          - `AvatarType`
          - `AvatarName`
          - `AvatarAttrib1`
          - `AvatarAttrib2`
          - `AvatarAttrib3`
          - `AvatarColor1`
          - `AvatarColor2`
          - `AvatarColor3`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `005` SendAccessoriesServer
      - Updates the Avatar Accessories variables in the player's save game, Called as player selects hats, outfits and other Avatar Accessories.
        - arguments:
          - `AvatarHat`
          - `AvatarCostume`
          - `AvatarTransport`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `006` SendBuddyServer
      - Updates the Avatar Buddy variables in the player's save game, Called as player selects an Avatar Buddy.
        - arguments:
          - `AvatarBuddy`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `007` SendMiniGameServer
      - Updates the MinigamesList variable in the player's save game, Called as player unlocks Minigames.
        - arguments:
          - `MinigamesList`
          - `HudPopularity`
          - `PersonalMinigame`
          - `PersonalMode`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `008` SendMiniGameScoreServer
      - Updates the players Personal High scores for selected Minigame, Called after at the end of every Minigame.
        - arguments:
          - `PersonalMinigame`
          - `PersonalMode`
          - `PersonalHighscoreUpdate`
          - `WorldScore`
          - `PersonalFriend1`
          - `PersonalScore1`
          - `PersonalFriend2`
          - `PersonalScore2`
          - `PersonalFriend3`
          - `PersonalScore3`
          - `PersonalFriend4`
          - `PersonalScore4`
          - `PersonalFriend5`
          - `PersonalScore5`
          - `PersonalFriend6`
          - `PersonalScore6`
          - `PersonalFriend7`
          - `PersonalScore7`
          - `PersonalFriend8`
          - `PersonalScore8`
          - `PersonalFriend9`
          - `PersonalScore9`
          - `PersonalFriend10`
          - `PersonalScore10`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `009` LogOut
      - Logs the player out of the game, Called after the idle timeout has been reached.
        - arguments:
          - none
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `010` LogOutTime
      - Confirms the user is still authenticated, Called every 30 seconds.
        - arguments:
          - none
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `011` SendAlbum
      - Updates the PhotosList variables in the player's Photo Albums, Called as the player adds photos into thier Photo Albums.
        - arguments:
          - `AlbumID`
          - `PhotosList`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `012` SendFurnitureServer
      - Updates the FurnitureList in the player's save game, Called as the player unlocks various items of furniture during the course of Gameplay.
        - arguments:
          - `FurnitureList`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `013` SendInitialServer
      - This function sets multiple variables in the player's save game, Called once when player first logs into the game, sets all save game variables to an initial state.
        - arguments:
          - `HudCitizenship`
          - `HudFriendship`
          - `HudPopularity`
          - `Duty1Type`
          - `Duty1Total`
          - `Duty1Value`
          - `Duty2Type`
          - `Duty2Total`
          - `Duty2Value`
          - `Duty3Type`
          - `Duty3Total`
          - `Duty3Value`
          - `FavorDone`
          - `FavorType`
          - `FavorStep`
          - `FavorChar`
          - `FavorRecip`
          - `FavorObject`
          - `FavorWilt`
          - `FavorEduardo`
          - `FavorFrankie`
          - `FavorMac`
          - `FavorLastType`
          - `AdventuresList`
          - `AdventureType`
          - `AdventureStep`
          - `AdventureDate`
          - `AvatarChosen`
          - `AvatarType`
          - `AvatarName`
          - `AvatarAttrib1`
          - `AvatarAttrib2`
          - `AvatarAttrib3`
          - `AvatarColor1`
          - `AvatarColor2`
          - `AvatarColor3`
          - `AvatarHat`
          - `AvatarBuddy`
          - `AvatarCostume`
          - `AvatarTransport`
          - `MinigamesList`
          - `Album1List`
          - `Album2List`
          - `Album3List`
          - `Album4List`
          - `Album5List`
          - `FurnitureList`
          - `BirthdayHat`
          - `NewBirthdayHat`
          - `MusicTrack`
          - `AvatarRoom`
          - `CodesList`
          - `ObjectsList`
          - `MyBestFriendPhotoList`
          - `ToysList`
          - `Bus`
          - `BestFriendCode`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `014` SendTracker
      - Tracker used for debugging, Called when user plays a Minigame.
        - arguments:
          - `Minigame`
          - `Mode`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `015` SendHatBornServer
      - Updates the BirthdayHat variables in the player's savegame, Called if player logs in on the day and month the player set during Registration.
        - arguments:
          - `BirthdayHat`
          - `NewBirthdayHat`
          - `HudPopularity`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `016` SendMusicTrackServer
      - Sets the MusicTrack variables in the player's savegame, Called as player selects different music tracks in Notey.
        - arguments:
          - `MusicTrack`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `017` SendDutiesLoginServer
      - Sets the Duty variables in the player's savegame, Called at login to create new duties for the player.
        - arguments:
          - `Duty1Type`
          - `Duty1Total`
          - `Duty1Value`
          - `Duty2Type`
          - `Duty2Total`
          - `Duty2Value`
          - `Duty3Type`
          - `Duty3Total`
          - `Duty3Value`
          - `DutiesUpdate`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `018` SendAvatarRoom
      - Sets the AvatarRoom variable in the player's savegame, When called enables or disables access to the the Avatar's room in the Mansion.
        - arguments:
          - `AvatarRoom`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `019` SendCodesList
      - Updates the CodesList variable in the player's savegame, Called when player enters a valid Secret Code into Notey.
        - arguments:
          - `CodesList`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `020` - SendObjectsList
      - Updates the ObjectsList variable in the player's savegame, Called when player uses tickets in the Prize Hive in the Shopping Mall.
        - arguments:
          - `ObjectsList`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `021` SendMyBestFriendPhotoList
      - Updates the MyBestFriendPhotoList variable in the player's savegame, Called when player unlocks a Photo in the Best Friend Photo Album.
        - arguments:
          - `MyBestFriendPhotoList`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `022` SendToysList
      - Updates the ToysList variable in the player's savegame, Called when player unlocks a Toy from the Toy Chest in Mac's room.
        - arguments:
          - `ToysList`
          - `HudPopularity`
        - returns:
          -`0` = operation successful / `1` = operation failed
    - `023` SendTracker
      - Tracker used for debugging, Called when player interacts with a Toy in the Toy Chest in Mac's room.
        - arguments:
          -`Toys`
        - returns:
          - `0` = operation successful / `1` = operation failed
    - `024` SendBus
      - Sets the Bus variable in the player's savegame, When called enables or disables the Foster's bus to apear outside the house, enables players to visit locations around town.
        - arguments:
          - `Bus`
        -  returns:
          - `0` = operation successful / `1` = operation failed
    - `101` mGetMiniGameServer
      - Provides highscores for selected Minigame, return the highscores of the player for each dificulty level, followed by the world highscores for each game dificulty level.
        After Savegame version 140 the players Bestfriend highest score for game dificulty level was added.
      - arguments:
        - `Minigame`
      - returns:
        - `0` = operation successful / `1` = operation failed
        - `Mode1BestFriendBestHighscore`
        - `Mode2BestFriendBestHighscore`
        - `Mode3BestFriendBestHighscore`
        - `Mode1PersonalFriend1`
        - `Mode1PersonalFriend2`
        - `Mode1PersonalFriend3`
        - `Mode1PersonalFriend4`
        - `Mode1PersonalFriend5`
        - `Mode1PersonalFriend6`
        - `Mode1PersonalFriend7`
        - `Mode1PersonalFriend8`
        - `Mode1PersonalFriend9`
        - `Mode1PersonalFriend10`
        - `Mode1PersonalScore1`
        - `Mode1PersonalScore2`
        - `Mode1PersonalScore3`
        - `Mode1PersonalScore4`
        - `Mode1PersonalScore5`
        - `Mode1PersonalScore6`
        - `Mode1PersonalScore7`
        - `Mode1PersonalScore8`
        - `Mode1PersonalScore9`
        - `Mode1PersonalScore10`
        - `Mode2PersonalScore1`
        - `Mode2PersonalScore2`
        - `Mode2PersonalScore3`
        - `Mode2PersonalScore4`
        - `Mode2PersonalScore5`
        - `Mode2PersonalScore6`
        - `Mode2PersonalScore7`
        - `Mode2PersonalScore8`
        - `Mode2PersonalScore9`
        - `Mode2PersonalScore10`
        - `Mode2PersonalFriend1`
        - `Mode2PersonalFriend2`
        - `Mode2PersonalFriend3`
        - `Mode2PersonalFriend4`
        - `Mode2PersonalFriend5`
        - `Mode2PersonalFriend6`
        - `Mode2PersonalFriend7`
        - `Mode2PersonalFriend8`
        - `Mode2PersonalFriend9`
        - `Mode2PersonalFriend10`
        - `Mode3PersonalScore1`
        - `Mode3PersonalScore2`
        - `Mode3PersonalScore3`
        - `Mode3PersonalScore4`
        - `Mode3PersonalScore5`
        - `Mode3PersonalScore6`
        - `Mode3PersonalScore7`
        - `Mode3PersonalScore8`
        - `Mode3PersonalScore9`
        - `Mode3PersonalScore10`
        - `Mode3PersonalFriend1`
        - `Mode3PersonalFriend2`
        - `Mode3PersonalFriend3`
        - `Mode3PersonalFriend4`
        - `Mode3PersonalFriend5`
        - `Mode3PersonalFriend6`
        - `Mode3PersonalFriend7`
        - `Mode3PersonalFriend8`
        - `Mode3PersonalFriend9`
        - `Mode3PersonalFriend10`
        - `Mode1WorldFriend1`
        - `Mode1WorldFriend2`
        - `Mode1WorldFriend3`
        - `Mode1WorldFriend4`
        - `Mode1WorldFriend5`
        - `Mode1WorldFriend6`
        - `Mode1WorldFriend7`
        - `Mode1WorldFriend8`
        - `Mode1WorldFriend9`
        - `Mode1WorldFriend10`
        - `Mode1WorldScore1`
        - `Mode1WorldScore2`
        - `Mode1WorldScore3`
        - `Mode1WorldScore4`
        - `Mode1WorldScore5`
        - `Mode1WorldScore6`
        - `Mode1WorldScore7`
        - `Mode1WorldScore8`
        - `Mode1WorldScore9`
        - `Mode1WorldScore10`
        - `Mode2WorldScore1`
        - `Mode2WorldScore2`
        - `Mode2WorldScore3`
        - `Mode2WorldScore4`
        - `Mode2WorldScore5`
        - `Mode2WorldScore6`
        - `Mode2WorldScore7`
        - `Mode2WorldScore8`
        - `Mode2WorldScore9`
        - `Mode2WorldScore10`
        - `Mode2WorldFriend1`
        - `Mode2WorldFriend2`
        - `Mode2WorldFriend3`
        - `Mode2WorldFriend4`
        - `Mode2WorldFriend5`
        - `Mode2WorldFriend6`
        - `Mode2WorldFriend7`
        - `Mode2WorldFriend8`
        - `Mode2WorldFriend9`
        - `Mode2WorldFriend10`
        - `Mode3WorldScore1`
        - `Mode3WorldScore2`
        - `Mode3WorldScore3`
        - `Mode3WorldScore4`
        - `Mode3WorldScore5`
        - `Mode3WorldScore6`
        - `Mode3WorldScore7`
        - `Mode3WorldScore8`
        - `Mode3WorldScore9`
        - `Mode3WorldScore10`
        - `Mode3WorldFriend1`
        - `Mode3WorldFriend2`
        - `Mode3WorldFriend3`
        - `Mode3WorldFriend4`
        - `Mode3WorldFriend5`
        - `Mode3WorldFriend6`
        - `Mode3WorldFriend7`
        - `Mode3WorldFriend8`
        - `Mode3WorldFriend9`
        - `Mode3WorldFriend10`
    - `102` ValidateName
      - Validates the player provided Avatar Name Checking for offensive/inappropriate words, Called when player Sets or changes Avatar name.
        - arguments:
          - `AvatarName`
        - returns:
          - `0` = Provided name valid / `1` = Provided name invalid
    - `103` GetFirstTimeState
      - Returns the current players savegame, Called once during preloading.
        - arguments:
          - none
        - returns:
          - `0` = operation successful / `1` = Best Friend Code invalid
          - Number of days since last login
          - Todays Date (in YYYYMMDD format)
          - IDLE_TIMEOUT
          - Players birthday (in 2000MMDD format)
          - `AvatarCode`
          - `AvatarChosen`
          - `AvatarType`
          - `AvatarName`
          - `AvatarAttrib1`
          - `AvatarAttrib2`
          - `AvatarAttrib3`
          - `AvatarColor1`
          - `AvatarColor2`
          - `AvatarColor3`
          - `AvatarHat`
          - `AvatarBuddy`
          - `AvatarCostume`
          - `AvatarTransport`
          - `HudCitizenship`
          - `HudFriendship`
          - `HudPopularity`
          - `Duty1Type`
          - `Duty1Value`
          - `Duty1Total`
          - `Duty2Type`
          - `Duty2Value`
          - `Duty2Total`
          - `Duty3Type`
          - `Duty3Value`
          - `Duty3Total`
          - `FavorDone`
          - `FavorLastType`
          - `FavorWilt`
          - `FavorEduardo`
          - `FavorFrankie`
          - `FavorMac`
          - `FavorType`
          - `FavorStep`
          - `FavorChar`
          - `FavorRecip`
          - `FavorObject`
          - `AdventuresList`
          - `AdventureType`
          - `AdventureStep`
          - `AdventureDate`
          - `MinigamesList`
          - `MiniGame1Mode1PersonalBestHighscore`
          - `MiniGame1Mode2PersonalBestHighscore`
          - `MiniGame1Mode3PersonalBestHighscore`
          - ...
          - ...
          - ...
          - `MiniGame99Mode1PersonalBestHighscore`
          - `MiniGame99Mode2PersonalBestHighscore`
          - `MiniGame99Mode3PersonalBestHighscore`
          - `PhotosList1`
          - `PhotosList2`
          - `PhotosList3`
          - `PhotosList4`
          - `PhotosList5`
          - `FurnitureList`
          - `BirthdayHat`
          - `NewBirthdayHat`
          - `MusicTrack`
          - `AvatarRoom`
          - `CodesList`
          - `ObjectsList`
          - `MyBestFriendPhotoList`
          - `ToysList`
          - `Bus`
          - `BestFriendCode`
          - `BestFriendAvatarType`
          - `BestFriendAvatarName`
          - `BestFriendAvatarAttrib1`
          - `BestFriendAvatarAttrib2`
          - `BestFriendAvatarAttrib3`
          - `BestFriendAvatarColor1`
          - `BestFriendAvatarColor2`
          - `BestFriendAvatarColor3`
          - `BestFriendAvatarHat`
          - `BestFriendAvatarBuddy`
          - `BestFriendAvatarCostume`
          - `BestFriendAvatarTransport`
    - `104` ValidateBestFriendAvatarCode
      - Validates the user provided Best Friend Code, returns Avatar attributes if valid.
        - arguments:
          - `BestFriendCode`
        - returns:
          - `0` = operation successful / `1` = Best Friend Code invalid
          - `BestFriendCode`
          - `AvatarType`
          - `AvatarName`
          - `AvatarAttrib1`
          - `AvatarAttrib2`
          - `AvatarAttrib3`
          - `AvatarColor1`
          - `AvatarColor2`
          - `AvatarColor3`
          - `AvatarHat`
          - `AvatarBuddy`
          - `AvatarCostume`
          - `AvatarTransport`