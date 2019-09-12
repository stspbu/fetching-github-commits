# fetching-github-commits
JetBrains autumn internship 2019 

## About
This program loads commits from a given git repository and stores code changes in local files. 
Some statistics about loaded commits is also stored.

## Requirements:
python3

## Usage examples
Basic usage:<br>
*python3 main.py fetch https://github.com/stspbu/fetching-github-commits*

Advanced usage:<br>
*python3 main.py settings set \[key:value\]* -- for change settings<br> 
*python3 main.py settings get* -- shows all available settings and their values<br>
*python3 main.py settings list* -- gives available settings list<br>

You can see all available commands in any time in your terminal. For that, type: <br>
*python3 main.py help*<br>
*python3 main.py settings help*

Available settings:<br>
folder -- folder, storing commit patches (default: files)<br>
token -- oauth token for github api, if requests limit exceeded<br>
statfile -- a file name, where last query statistics will be stored (default: stat)<br>
authorizedonly -- if set to 1, only authorized commit authors will be shown in stats (default: 0)<br>

## Project structure
*commands* folder contains modules for handling terminal commands<br>
*github* contains main classes for getting data from Github
*main.py* running the program and handles exceptions<br>
*models* contains project models<br>
*settings* loads settings.json, provides methods for getting settings and writing them into settings.json
*storager* contains classes, which store stats and code changes in local files<br>