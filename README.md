# Charmed
Charmed is a text-based roguelike written in Python for a computer
game development class. The goal is to escape the dungeon with the
Charm of Relativity found on the ninth level. The random generation
is seeded, given difficulty, and balanced to be extremely difficult.

## Prerequisites
Charmed has been tested on Python 3.7. If anybody tests it on another
version, make a pull request of this file giving the lowest version
Charmed works on
### Windows
My program is untested on windows. If any issues occur, submit them
to the issue tracker on the repository
### Mac
Go into System Preferences > Security and Privacy > Privacy.
Click the lock and enter your password
Under accessibility, click the + button beneath the list.
A window will pop up showing all your applications. Find Terminal
in the Utilities folder and double-click on it.

This will allow Charmed to get keyboard events when it is running.
This is necessary because you don't want to press enter after every
movement command.

## Running
### Windows
At the moment, I haven't created a batch script to run the program.
If someone would like to do this, make a pull request. The script
must run `main.py` in the terminal with Python 3
### Mac
Download the repository from the downloads section in the sidebar.
Double-click on `run.command`. If you get an error message saying
the file isn't executable, navigate to the directory in terminal and
run `chmod +x run.command`. Then run it. The game then explains
the rest.