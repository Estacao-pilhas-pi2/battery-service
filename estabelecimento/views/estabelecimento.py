from rest_framework.generics import CreateAPIView

from estabelecimento.serializers.estabelecimento import EstabelecimentoSerializer


class EstabelecimentoCadastroView(CreateAPIView):
    serializer_class = EstabelecimentoSerializer
