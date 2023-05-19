from rest_framework.generics import CreateAPIView

from maquina.serializers.maquina import MaquinaSerializer


class MaquinaCadastroView(CreateAPIView):
    serializer_class = MaquinaSerializer
