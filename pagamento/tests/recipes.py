from model_bakery.recipe import Recipe

from pagamento.models import Pagamento

pagamento = Recipe(Pagamento, _fill_optional=True)
