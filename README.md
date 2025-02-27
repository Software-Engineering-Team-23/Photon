#### First install Tkinter, psycopg2, and PIL

#### If you don't have pip, please install it with "sudo apt install python3-pip"

#### PIL package is required

Type in Command Prompt:

pip install Pillow

Alternatively on Debian:

sudo apt install python3-pil python3-pil.imagetk

#### Tkinter required

Debian:
sudo apt-get install python3-tk

MacOS:
brew install python-tk

#### psycopg2 required

Debian:
sudo apt install python3-psycopg2

MacOS:
brew install postgresql
pip install psycopg2

#### After installed, type "python3 udp.py" in one terminal.
#### Then in a different terminal, type "python3 main.py"
#### Once at the player entry screen, enter the player ID in the left field.
#### Then, in the right field, enter the equipment ID, which will transmit to UDP.
#### The database will be updated accordingly.


GitHub	          |  Name            | Part of project
:----------------:|:----------------:|:------------:
alexRAI10	        |  Alain Delgado   | splash_screen
dylan-schlageter  | Dylan Schlageter | first_screen/udp
nnwp-ross	        |  Jordan Calhoun  | sql/database
m-lm	            |  Micah McCollum  | splash-first screen transition, rework entry flow
RAndreChavez	    |  Remer Chavez    |
