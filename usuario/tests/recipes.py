from model_bakery.recipe import Recipe

from usuario.models import Usuario


usuario = Recipe(Usuario, telefone='5561912345678', _fill_optional=True)
