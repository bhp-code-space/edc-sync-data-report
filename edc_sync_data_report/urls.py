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
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from edc_identifier.admin_site import edc_identifier_admin

from edc_sync_data_report.views.client_view_summary_api import \
    GetLiveClientSyncSummaryAPI, ListClientSyncSummaryAPI
from edc_sync_data_report.views.report_summary_view import ReportSummaryView, \
    ReportSummaryViewAPI
from edc_sync_data_report.views.sync_confirmation_ids_view_api import \
    SyncConfirmationIdsViewAPI
from edc_sync_data_report.views.sync_detailed_report_view import SyncDetailedReportView, \
    SyncSiteListView
from .views import AdministrationView, HomeView

app_name = 'edc_sync_data_report'

urlpatterns = [

    path('active_sync_sites/', SyncSiteListView.as_view()),
    path('api/live_data/', GetLiveClientSyncSummaryAPI.as_view()),
    path('report_summary/', ReportSummaryView.as_view()),
    path('api/<str:server>/<int:site_id>/report_summary/',
         ReportSummaryViewAPI.as_view()),
    path('<str:server>/<int:site_id>/<str:created_date>/detailed_report/',
         SyncDetailedReportView.as_view()),
    path('api/client_summary/', ListClientSyncSummaryAPI.as_view()),
    path('api/<int:site_id>/<str:created_date>/confirmation_data/',
         SyncConfirmationIdsViewAPI.as_view()),
    path('admin/', admin.site.urls),
    path('admin/', edc_identifier_admin.urls),
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('edc_base/', include('edc_base.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('home/', HomeView.as_view(), name='home_url'),
    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='logout'),
    path('', HomeView.as_view(), name='home_url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

INDEX_PAGE = 'localhost:8000'
