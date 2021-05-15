# bfahps

Big Fat Awesome House Party was an online game created by Powerful Robot Games featuring the characters of Foster's Home for Imaginary Friends. 

The game began on May 15th, 2006, and updated monthly.  Originally intended to end on April 16th, 2007, the game was later extended to October 15th, 2007.

This python package simulates the Big Fat Awesome House Party server, providing a local webserver instance to serve both static assets and the dynamic services required to play the game.


## Required files

Game assets need to be installed into the htdocs folder.  These files are copyrighted and are not included in this distribution, users will need to find the files for themselves, I'm not able to provide you with the files.

You need both the toon directory from i.cartoonnetwork.com, and the toonahp directory from i.awesomehouseparty.com to play the game.


## Configuration

Depending on the version of toonahp your have installed you may need to edit the settings in config.py

SAVE_VERSION is the only variable you should need to change, set it to 140 if you have a version of toonahp after the Best Friend Code feature was added (v1.14.3 or higher)


## Usage
You should have Python3 with the Flask and Flask-SQLAlchemy libraries installed.

If you have `pipenv` installed, then you can do:
```shell
pipenv --three
pipenv install
pipenv run python3 server.py
```

Otherwise start the server with this command:

```shell
python3 server.py
```
Then launch a web-browser with Abobe Flash and Shockwave Director plugins enabled to URL that appears in the server output, this is usually http://localhost:5000/