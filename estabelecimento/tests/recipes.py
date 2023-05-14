from model_bakery.recipe import Recipe

from estabelecimento.models import Estabelecimento


estabelecimento = Recipe(Estabelecimento, _fill_optional=True)
