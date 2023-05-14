from model_bakery.recipe import Recipe

from reciclador.models import Reciclador


reciclador = Recipe(Reciclador, _fill_optional=True)
