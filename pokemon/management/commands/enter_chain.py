import requests
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon
import re


def get_chain(chain):
    url = 'https://pokeapi.co/api/v2/evolution-chain/{}/'.format(chain)
    r = requests.get(url, headers={'Content-Type': 'application/json'})
    chain = r.json()
    query = chain['chain']
    count = 1
    data = []
    while query != []:
        try:
            id = re.findall(
                '[0-9]+', query.get('species').get('url'))[1]
            pokemon = get_pokemon(id)
            pokemon['evolve'] = count
            pokemon['chain-id'] = chain['id']
            data.append(pokemon)
            count += 1
            if len(query['evolves_to']) > 1 and count > 1:
                for i in range(0, len(query['evolves_to'])):
                    id = re.findall(
                        '[0-9]+', query['evolves_to'][i].get('species').get('url'))[1]
                    pokemon = get_pokemon(id)
                    pokemon['evolve'] = count
                    pokemon['chain-id'] = chain['id']
                    data.append(pokemon)
            query = query['evolves_to'][0]
        except IndexError:
            break
    data = [i for n, i in enumerate(data) if i not in data[n + 1:]]
    return data


def save_pokemon(chain):

    for data in get_chain(chain):
        try:
            pokemon = Pokemon(
                name=data['name'],
                apiId=data['api-id'],
                chainId=data['chain-id'],
                healtPoint=data['hp'],
                attack=data['attack'],
                defense=data['defense'],
                specialAttack=data['special-attack'],
                specialDefense=data['special-defense'],
                speed=data['speed'],
                height=data['height'],
                weight=data['weight'],
                evolution=data['evolve']
            )
            pokemon.save()
        except Exception:
            print("repeated")


def get_pokemon(id):
    data = {
        'api-id': 0,
        'chain-id': 0,
        'name': '',
        'hp': 0,
        'attack': 0,
        'defense': 0,
        'special-attack': 0,
        'special-defense': 0,
        'speed':  0,
        'height': 0,
        'weight': 0,
        'evolve': 0
    }
    url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(id)
    r = requests.get(url, headers={'Content-Type': 'application/json'})
    pokemon = r.json()
    data['api-id'] = pokemon['id']
    data['name'] = pokemon['species']['name']
    data['hp'] = pokemon['stats'][0]['base_stat']
    data['attack'] = pokemon['stats'][1]['base_stat']
    data['defense'] = pokemon['stats'][2]['base_stat']
    data['special-attack'] = pokemon['stats'][3]['base_stat']
    data['special-defense'] = pokemon['stats'][4]['base_stat']
    data['speed'] = pokemon['stats'][5]['base_stat']
    data['height'] = pokemon['height']
    data['weight'] = pokemon['weight']
    return data


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
        save_pokemon(enter_int())
        q = question()
        while q:
            save_pokemon(enter_int())
            q = question()
        print("completed")
