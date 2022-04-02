"""edc_sync_data_report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from edc_identifier.admin_site import edc_identifier_admin

from .views import HomeView, AdministrationView

app_name = 'edc_sync_data_report'

from edc_sync_data_report.views.client_view_summary_api import ListClientSyncSummaryAPI, GetLiveClientSyncSummaryAPI


urlpatterns = [
    path('client_summary/', ListClientSyncSummaryAPI.as_view()),
    path('live_data/', GetLiveClientSyncSummaryAPI.as_view()),
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', admin.site.urls),
    path('admin/', edc_identifier_admin.urls),
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('edc_base/', include('edc_base.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
