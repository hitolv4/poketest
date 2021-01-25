
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Pokemon


def pokemon_list(request):
    pokemon = Pokemon.objects.all()
    data = {"results": list(pokemon.values(
        "name",
        "apiId",
        "chainId",
        "healtPoint",
        "attack",
        "defense",
        "specialAttack",
        "specialDefense",
        "speed",
        "height",
        "weight",
        "evolution"
    ))
    }
    return JsonResponse(data)


def pokemon_detail(request, name):
    pokemon = get_object_or_404(Pokemon, name=name)
    chain = Pokemon.objects.values('name', 'apiId', 'evolution').filter(
        chainId=pokemon.chainId).exclude(name=pokemon.name)

    data = {"Pokemon": {
        "name": pokemon.name,
        "apiId": pokemon.apiId,
        "chainId": pokemon.chainId,
        "healtPoint": pokemon.healtPoint,
        "attack": pokemon.attack,
        "defense": pokemon.defense,
        "specialAttack": pokemon.specialAttack,
        "specialDefense": pokemon.specialDefense,
        "speed": pokemon.speed,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "evolution": pokemon.evolution
    },
        "evolution": []
    }

    for i in chain:
        et = ""
        if i["evolution"] > pokemon.evolution:
            et = "Evolution"
        elif i["evolution"] < pokemon.evolution:
            et = "Preevolution"
        else:
            et = "Alternate"
        related = {
            "apiId": i["apiId"],
            "name": i["name"],
            "type": et
        }
        data['evolution'].append(related)

    return JsonResponse(data)
