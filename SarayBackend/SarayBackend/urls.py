from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = 'SARAY PHOTOSTUDIO'
admin.site.index_title = 'Личный кабинет'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v0/', include('api_v0.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)