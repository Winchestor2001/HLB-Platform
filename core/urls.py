from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from .yasg import urlpatterns as yasg_urlpatterns
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('audit_site.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/student/', include('student_platform.urls')),
    path('api/payment/', include('click_payment.urls')),
    path('api/admin/', include('admin_platform.urls')),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += yasg_urlpatterns

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('audit_site.urls')),
    prefix_default_language=False
)
