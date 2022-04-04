from edc_sync_data_report.classes.summary_data import SummaryData
from edc_sync_data_report.models import ClientSyncSummary


class ClientCollectSummaryData(SummaryData):

    def create_summary_data(self):
        if len(self.build_summary()) > 0:
            return ClientSyncSummary.objects.create(
                name='ranaka', # fixme set site name
                data=self.build_summary())
