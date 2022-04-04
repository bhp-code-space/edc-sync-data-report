import requests

from django.views import View

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from django.http import HttpResponse


from datetime import datetime

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from edc_sync_data_report.classes import ReportSummaryData
from edc_sync_data_report.classes.row_data import RowData
from edc_sync_data_report.classes.server_collect_summary_data import ServerCollectSummaryData
from edc_sync_data_report.models import SyncAPIs, SyncSite
from edc_sync_data_report.serializers import SyncSummarySerializer


class ReportSummaryView(TemplateView): #, LoginRequiredMixin, EdcBaseViewMixin):

    template_name = 'data_summary_report.html'
    # navbar_name = 'flourish_reports'
    # navbar_selected_item = 'flourish_reports'

    # def get_success_url(self):
    #     return reverse('flourish_reports:recruitment_report_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # summary_api = SyncAPIs.objects.get(sync_site__identifier=identifier, sync_site__valid_to__lte=datetime.today(),
        #                                name="summary_api")
        # response = requests.get(summary_api.uri)
        # client_data = response.json()
        #
        # server_report = ServerCollectSummaryData()
        # server_data = server_report.build_summary(site_id=summary_api[0].site.site_id)
        #
        # report = ReportSummaryData(server_data=server_data, client_data=client_data)
        # matching, not_matching = report.data_comparison()
        data = []
        row = RowData( 'Subject Visit', 10235, 10235, label='Matching')
        data.append(row)
        row = RowData('Caregiver', 10235, 10235, label='Matching')
        data.append(row)
        row = RowData('Locator', 1023225, 222244, label='Not matching')
        data.append(row)
        row = RowData('Contact', 10235, 10235, label='Matching')
        data.append(row)
        row = RowData('Referral', 10235, 10235, label='Matching')
        data.append(row)
        row = RowData('Locator Info', 1023225, 22222, label='Not matching')
        data.append(row)
        row = RowData('Locator', 1023225, 222244, label='Not matching')
        data.append(row)
        context['sync_report'] = data
        context['sync_sites'] = SyncSite.objects.all()

        # Fixme I need list of sites
        return context

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

from django.core import serializers

class ReportSummaryViewAPI(APIView): #, LoginRequiredMixin, EdcBaseViewMixin):

    template_name = 'data_summary_report.html'

    def get(self, request, format=None, identifier=None):
        print(request)
        data = []
        row = RowData('Contact', 10235, 10235, label='Matching')
        data.append(row)
        row = RowData('Referral', 10235, 10235, label='Matching')
        data.append(row)
        row = RowData('Locator Info', 1023225, 22222, label='Not matching')
        data.append(row)
        row = RowData('Locator', 1023225, 222244, label='Not matching')
        data.append(row)
        serializer = SyncSummarySerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
