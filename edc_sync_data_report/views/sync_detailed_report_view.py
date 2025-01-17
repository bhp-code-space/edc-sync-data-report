import csv
from datetime import datetime

import requests
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.base import View

from edc_sync_data_report.classes.does_transaction_exists_in_central_server import \
    DoesTransactionExistsInCentralServer
from edc_sync_data_report.models import SyncSite


class SyncSiteListView(TemplateView):  # , LoginRequiredMixin, EdcBaseViewMixin):

    template_name = 'sync_sites_list.html'  # Todo finish view list for active communities

    def get_context_data(self, **kwargs):
        active_sync_sites = SyncSite.objects.filter(
            Q(valid_to__gte=datetime.today()) | Q(valid_to__isnull=True))
        context = super().get_context_data(**kwargs)
        context['active_sync_sites'] = active_sync_sites
        return context


class SyncDetailedReportView(View):  # , LoginRequiredMixin, EdcBaseViewMixin):

    def get(self, request, *args, **kwargs):
        data = []
        site_id = kwargs.get('site_id')
        created_date = kwargs.get('created_date')
        server = kwargs.get('server')
        response = None
        sync_site = SyncSite.objects.filter(site__id=site_id).first()
        try:
            url = (f"http://{server}/edc_sync_data_report/api/{site_id}/"
                   f"{created_date}/confirmation_data/")
            response = requests.get(url, timeout=45)
            data = response.json()
            run_validation = DoesTransactionExistsInCentralServer()  # Fixme name of class
            missing_records = run_validation.sync_data_check(data=data)
            response = HttpResponse(content_type='text/csv')
            response[
                'Content-Disposition'] = (f'attachment; filename="missing_r'
                                          f'ecords-{site_id}-{created_date}.csv"')

            writer = csv.writer(response)
            writer.writerow(['Community Name', 'Site ID', '', ''])
            writer.writerow([sync_site.name, sync_site.community_site_id, '', ''])
            writer.writerow(['Model Name', 'App Label', 'Primary Key', 'Created Date'])
            for record in missing_records:
                writer.writerow(
                    [record["model_name"], record["app_label"], record["primary_key"],
                     record["data_collection_date"]])
        except requests.exceptions.Timeout:
            pass
        return response
