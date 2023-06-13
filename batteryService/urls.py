from django.contrib import admin
from django.urls import include, re_path

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


url_api = []
for app in settings.LOCAL_APPS:
    url_api.append(re_path(r'^', include(f'{app}.urls')))

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(url_api)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
