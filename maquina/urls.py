from django.urls import re_path, include

from maquina.views import maquina


urlpatterns = [
    re_path(r'^maquina/', include([
        re_path(r'^$', maquina.MaquinaListView.as_view(), name='maquina-list'),
        re_path(r'esvaziar/$', maquina.MaquinaEsvaziarView.as_view(), name='maquina-esvaziar'),
        re_path(r'(?P<pk>[\w\d]+)/$', maquina.MaquinaUpdateRetrieveView.as_view(), name='maquina-update-retrieve')
    ])),
]
