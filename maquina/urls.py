from django.urls import re_path, include

from maquina.views import maquina


urlpatterns = [
    re_path(r'^maquina/', include([
        re_path(
            r'^$', maquina.MaquinaCadastroView.as_view(),
            name='maquina-create'
        ),
    ])),
]
