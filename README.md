# Name

PokeTest

## Installation

pip install -r requirements.txt

## Usage

create virtualenv
source bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py enter_chain to save pokemons in the data base
enter evolution chain (id number of evolution chain from pokeapi.co)
then go to http://127.0.0.1:8000/pokemon/{name} in your browser
