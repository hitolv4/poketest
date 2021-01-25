from django.urls import path, include
from .views import pokemon_list, pokemon_detail


urlpatterns = [
    path('all', pokemon_list, name="pokemon_list"),
    path('<str:name>', pokemon_detail, name="pokemon_detail")
]
