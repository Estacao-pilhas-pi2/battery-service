from django.urls import re_path, include

from estabelecimento.views import estabelecimento


urlpatterns = [
    re_path(r'^estabelecimento/', include([
        re_path(
            r'^$', estabelecimento.EstabelecimentoCadastroView.as_view(),
            name='estabelecimento-create'
        ),
    ])),
]
