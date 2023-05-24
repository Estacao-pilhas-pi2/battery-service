from django.urls import re_path, include

from reciclador.views import reciclador


urlpatterns = [
    re_path(r'^reciclador/', include([
        re_path(
            r'^$', reciclador.RecicladorCadastroView.as_view(),
            name='reciclador-create'
        ),
        re_path(
            r'^(?P<pk>[\w\d]+)/$', reciclador.RecicladorDetailView.as_view(),
            name='reciclador-detail'
        )
    ])),
]
