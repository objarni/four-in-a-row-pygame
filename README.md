# four-in-a-row-pygame
An experiment with TEA in Python/PyGame


What is this?
-------------

I wanted to try out The Elm Architecture (TEA) in Python, and chose to use PyGame as it contains all needed to make a small game.

The choice of 4-in-a-row is arbitrary, but big enough to contain animation, some logic and interaction with the user aswell as menu and game over scenes.

To make the code maintainable and easily refactorable, I choose to use Approval Tests for all test automation.

Running
-------

Install `requirements.txt`.

The game is started by running `main.py`.

Use pytest to run the tests.

The script `tests/accept_all_received.py` overwrites all approval.txt files with their received.txt equivalent, removing the latter. Be careful!
