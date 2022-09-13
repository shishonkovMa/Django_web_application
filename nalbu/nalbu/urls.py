from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from riddle.views import *
from nalbu import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('riddle.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
