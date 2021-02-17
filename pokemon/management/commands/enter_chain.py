import requests
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon
import re


class Pokemon_chain:
    def __init__(self, chain):
        self.chain = self.get_chain(chain)
        self.names = self.get_names(self.chain, chain)
        self.pokemons = self.get_pokemons(self.names)
        self.save = self.save_pokemon(self.pokemons)

    def get_chain(self, chain):
        url = f"https://pokeapi.co/api/v2/evolution-chain/{chain}/"
        r = requests.get(url, headers={'Content-Type': 'application/json'})
        chain = r.json()
        data = chain['chain']
        return data

    def get_names(self, data, id):
        data = data
        names = {}
        count = 1
        names[data.get('species').get('name')] = {
            'evolve': count,
            'chain-id': id
        }

        while data != []:
            try:
                count += 1
                if len(data['evolves_to']) == 1:
                    for i in range(0, len(data['evolves_to'])):
                        names[data['evolves_to'][i].get(
                            'species').get('name')] = {
                            'evolve': count,
                            'chain-id': id
                        }
                data = data['evolves_to'][0]
            except IndexError:
                break
        return names

    def get_pokemons(self, names):
        data = {}
        for k, v in names.items():
            url = f"https://pokeapi.co/api/v2/pokemon/{k}/"
            r = requests.get(url, headers={'Content-Type': 'application/json'})
            pokemon = r.json()
            data[k] = {
                'api-id': pokemon['id'],
                'chain-id': v['chain-id'],
                'name': pokemon['species']['name'],
                'hp': pokemon['stats'][0]['base_stat'],
                'attack': pokemon['stats'][1]['base_stat'],
                'defense': pokemon['stats'][2]['base_stat'],
                'special-attack': pokemon['stats'][3]['base_stat'],
                'special-defense': pokemon['stats'][4]['base_stat'],
                'speed':  pokemon['stats'][5]['base_stat'],
                'height': pokemon['height'],
                'weight': pokemon['weight'],
                'evolve': v['evolve']
            }
        return data

    def save_pokemon(self, pokemons):

        for pokemon in pokemons:
            try:
                pokemon = Pokemon(
                    name=pokemons[pokemon]['name'],
                    apiId=pokemons[pokemon]['api-id'],
                    chainId=pokemons[pokemon]['chain-id'],
                    healtPoint=pokemons[pokemon]['hp'],
                    attack=pokemons[pokemon]['attack'],
                    defense=pokemons[pokemon]['defense'],
                    specialAttack=pokemons[pokemon]['special-attack'],
                    specialDefense=pokemons[pokemon]['special-defense'],
                    speed=pokemons[pokemon]['speed'],
                    height=pokemons[pokemon]['height'],
                    weight=pokemons[pokemon]['weight'],
                    evolution=pokemons[pokemon]['evolve']
                )
                pokemon.save()
            except Exception:
                print("repeated")


def enter_int():
    while True:
        try:
            chain = int(input("Please enter an evolution chain:\n"))
            return chain
        except:
            print("must enter a Integer")


def question():
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    while True:
        choice = input("enter another chain yes/no\n").lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no' ")


class Command(BaseCommand):
    def handle(self, *args, **options):
        Pokemon_chain(enter_int())
        q = question()
        while q:
            Pokemon_chain(enter_int())
            q = question()
        print("completed")
