# Space Game
A game engine for a space game. Animation of a spaceship controlled by arrows.
The standard library `curses` and asynchronous programming are used. 

![Example](ezgif.com-optimize_YgtCKU0.gif)

### How to install

Python 3 should already be installed.
The Windows terminal does not support part of the console graphics. Possible solutions:
* Use the `windows-curses` library
* Use the bash shell of the terminal/WSL

For Windows, create a virtual environment in the project directory:
```shell
python -m venv venv
```
Activate it.
```shell
.\venv\Scripts\activate
```
Install the Windows-curses library:
```shell
pip install windows-curses
```

### How to run the game
To start the game, run the following command in the terminal:
```shell
python space_game.py
```

### Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).