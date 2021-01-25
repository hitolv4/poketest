from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Pokemon(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    apiId = models.IntegerField(_("apiId"), unique=True)
    chainId = models.IntegerField(_("chainId"))
    healtPoint = models.IntegerField(_("healtPoint"))
    attack = models.IntegerField(_("attack"))
    defense = models.IntegerField(_("defense"))
    specialAttack = models.IntegerField(_("specialAttack"))
    specialDefense = models.IntegerField(_("specialDefense"))
    speed = models.IntegerField(_("speed"))
    height = models.IntegerField(_("height"))
    weight = models.IntegerField(_("weight"))
    evolution = models.IntegerField(_("evolution"))
    created = models.DateTimeField(auto_now_add=True)
