# Photon

This is the repository for Team 23's implementation of Photon for CSCE 35103.

## Setup

First install Tkinter, psycopg2, pygame, and PIL using the command line.

If you don't have pip on Debian, please install it with "sudo apt install python3-pip"

#### PIL (Pillow) package

Debian:  
sudo apt install python3-pil python3-pil.imagetk

Alternatively:  
pip install Pillow

#### Tkinter package

Debian:  
sudo apt-get install python3-tk

MacOS:  
brew install python-tk

#### psycopg2 package

Debian:  
sudo apt install python3-psycopg2

MacOS:  
brew install postgresql  
pip install psycopg2

#### pygame package

Debian:  
sudo apt-get install python3-pygame

Pip:  
pip install pygame

## Instructions

After installing all requirements, type "python3 main.py".
Once at the player entry screen, enter the player ID in the left field.
Then, in the right field, enter the equipment ID, which will transmit to UDP.
The database will update accordingly.
Once the players are entered, you can press the F5 button to start the game.
The countdown timer will begin, after which the play action screen appears. 
After the game ends, a back button will appear to return to the entry screen. 

## Team


GitHub	          |  Name            |
:----------------:|:----------------:|
alexRAI10	        |  Alain Delgado   |
dylan-schlageter  | Dylan Schlageter |
nnwp-ross	        |  Jordan Calhoun  |
m-lm	            |  Micah McCollum  |
RAndreChavez	    |  Remer Chavez    |
