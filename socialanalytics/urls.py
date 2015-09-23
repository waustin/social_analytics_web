from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import logout, home


urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),

    # Facebook Reports
    url(r'^facebook/', include('facebook_reports.urls')),

    # Filebrowser, DJ Admin, & Grappelli

    url(r'^admin/', include(admin.site.urls)),

    # Social Authentication URLs
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^logout/$', logout, name='logout'),
]

# UPLOAD MEDIA IN DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
