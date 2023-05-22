from django.urls import re_path, include

from pagamento.views import pagamento


urlpatterns = [
    re_path(r'^pagamento/', include([
        re_path(
            r'^$', pagamento.PagamentoCreateView.as_view(),
            name='pagamento-create'
        ),
        re_path(
            r'efetuar/$', pagamento.PagamentoEfetuarView.as_view(),
            name='pagamento-efetuar'
        )
    ])),
]
