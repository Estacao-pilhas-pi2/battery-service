from django.urls import re_path, include

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from estabelecimento.views import estabelecimento


urlpatterns = [
    re_path(r'^estabelecimento/', include([
        re_path(
            r'^$', estabelecimento.EstabelecimentoCadastroView.as_view(),
            name='estabelecimento-create'
        ),
        re_path(
            'celular', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}),
            name='estabelecimento-celular'
        ),
    ])),
]
