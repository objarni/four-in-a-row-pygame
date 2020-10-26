# four-in-a-row-pygame
An experiment with The Elm Architecture and Approvals in Python/PyGame originally by Olof (@objarni) later refactored and extended by Emily (@emilybache).


What is this?
-------------

Olof wanted to try out The Elm Architecture (TEA) in Python, and chose to use PyGame as it contains all needed to make a small game. 

The choice of 4-in-a-row is arbitrary, but big enough to contain animation, some logic and interaction with the user 
as well as scene switches (start and game over scenes).

To make the code maintainable and easily refactorable, Olof choose to use Approval Tests for all test automation. 
Emily advised on some design choices, and refactored the tests a little to enhance readability.

Running
-------

Install `requirements.txt`.

The game is started by running `main.py`.

Use pytest to run the tests.

    python -m pytest

