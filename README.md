# WebkinzBot
This is a bot for playing Webkinz mini-games

Currently only supports Cash Cow and gets around $350/hour

## Installation
```shell script
git clone https://github.com/TheLogicMaster/WebkinzBot.git
cd WebkinzBot
easy-install .
```

## Usage
```shell script
python WebkinzBot.py
```

## Configuration
OpenCV is used to search the screen for the game window boundaries and
buttons, so those images can be replaced to better fit one's setup or the tolerance
parameters in function calls for 'find_in_image' can be decreased to more freely
match images. The commented out lines can be uncommented to draw the OpenCV matches
to game.png for debugging.