from datetime import date

import requests
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from rest_framework.views import APIView

from edc_sync_data_report.classes import ReportSummaryData
from edc_sync_data_report.classes.server_collect_summary_data import \
    ServerCollectSummaryData
from edc_sync_data_report.models import SyncSite
from edc_sync_data_report.serializers import SyncSummarySerializer


class ReportSummaryView(TemplateView):  # , LoginRequiredMixin, EdcBaseViewMixin):

    template_name = 'data_summary_report.html'

    # navbar_name = 'flourish_reports'
    # navbar_selected_item = 'flourish_reports'

    # def get_success_url(self):
    #     return reverse('flourish_reports:recruitment_report_url')

    def get_context_data(self, **kwargs):
        data = []
        context = super().get_context_data(**kwargs)
        site = SyncSite.objects.filter(
            Q(valid_to__gte=date.today()) | Q(valid_to__isnull=True)).first()
        try:
            URL = f"http://{site.server}/edc_sync_data_report/api/live_data/"
            try:
                response = requests.get(URL)
                client_data = response.json()

                server_report = ServerCollectSummaryData()
                server_data = server_report.build_summary(site_id=site.site_id)
                report = ReportSummaryData(server_data=server_data,
                                           client_data=client_data)
                matching, not_matching = report.data_comparison()
                data = matching + not_matching
            except requests.exceptions.Timeout:
                pass
        except AttributeError:
            pass
        context['sync_report'] = data
        context['sync_sites'] = SyncSite.objects.filter(
            Q(valid_to__gte=date.today()) | Q(valid_to__isnull=True))
        return context


class ReportSummaryViewAPI(APIView):
    template_name = 'data_summary_report.html'

    def get(self, request, format=None, site_id=None, server=None):
        data = []
        URL = f"http://{server}/edc_sync_data_report/api/live_data/"
        try:
            response = requests.get(URL)
            client_data = response.json()

            server_report = ServerCollectSummaryData()
            server_data = server_report.build_summary(site_id=site_id)
            report = ReportSummaryData(server_data=server_data, client_data=client_data)
            matching, not_matching = report.data_comparison()
            data = matching + not_matching
            serializer = SyncSummarySerializer(data, many=True)
        except requests.exceptions.Timeout:
            pass
        return JsonResponse(serializer.data, safe=False)
