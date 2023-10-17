from edc_sync_data_report.classes.summary_data import SummaryData
from edc_sync_data_report.models import ClientSyncSummary


class ClientCollectSummaryData(SummaryData):
    """Build summary data by counting each model records then store in the JSON field.
        This is useful for project which
        are very large to build this report data.
    """

    def create_summary_data(self):
        data = self.build_summary()
        if len(data) > 0:
            return ClientSyncSummary.objects.create(
                data=data)
