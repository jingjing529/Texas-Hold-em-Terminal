# Texas-Hold-em-Terminal
Texas-Hold-em-Terminal is a Texas Hold'em poker card game with interactive features. It allows everyone to play Texas Hold'em in the terminal with inputted number of bot players.

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have installed the latest version of Python 3, or at least Python 3.8.2.
* You are familiar with the game Texas Hold'em. If not, here is a helpful resource: https://en.wikipedia.org/wiki/Texas_hold_%27em 

## Using Texas-Hold-em-Terminal
To play Texas-Hold-em-Terminal using user mode, follow these few steps.
1. Run the program by entering the number of bot players through command line as below:
Python Texas-Hold-em-Terminal.py -u -p number_of_bot_player
2. Follow the instructions in the program to take actions such as fold/bet/check.
3. The game will end under these kinds of circumstances:
* You don't want to start another round of game. (You decide to quit the game)
* There is no bot player left. (All bot players quit the game)
* You don't have enough money to player another round. (The game ends automatically.)

## Running tests
If you want to check the correctness of this game, you can use file mode to run the test cases using the following command. 
Python Texas-Hold-em-Terminal.py -f -i path_to_cases_directory
The output should be the number of tests passed.  
Note: path_to_cases_directory should contain a folder with all the test cases and a text_result.txt file.

## Contact
If you want to contact me you can reach me at jingjw23@uci.edu
