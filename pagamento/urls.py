from django.urls import re_path, include

from pagamento.views import pagamento


urlpatterns = [
    re_path(r'^pagamento/', include([
        re_path(
            r'^$', pagamento.PagamentoListCreateView.as_view(),
            name='pagamento-list-create'
        ),
        re_path(
            r'^efetuar/$', pagamento.PagamentoEfetuarView.as_view(),
            name='pagamento-efetuar'
        )
    ])),
]
