from django.urls import re_path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from usuario.views import token


urlpatterns = [
    re_path(r'^login/', include([
        re_path(r'^$', token.TokenObtainPairView.as_view(), name='usuario-login'),
        re_path(r'^refresh/$', TokenRefreshView.as_view(), name='usuario-refresh'),
        re_path(r'^verify/$', TokenVerifyView.as_view(), name='usuario-verify'),
    ])),

    # re_path(r'^usuario/', include([
    #     re_path(
    #         r'^(?P<id>)/$',
    #         usuario.UsuarioRetrieveUpdateAPIView.as_view(),
    #         name='usuario-details-update'
    #     ),
    # ]))
]
