from edc_sync_data_report.models import SyncModels, ClientSyncSummary
from django.apps import apps


class ClientCollectSummaryData(object):

    def count_by_app_label_and_model_name(self, app_label, model_name):
        model_cls = apps.get_model(app_label, model_name)
        return model_cls.objects.count()

    def build_summary(self):
        data = {}
        sync_models = SyncModels.objects.all()

        for sync_model in sync_models:
            key = f'{sync_model.app_label}__{sync_model.model_name}'
            model_data = {f'{key}': self.count_by_app_label_and_model_name(sync_model.app_label, sync_model.model_name)}
            data.update(model_data)
        return data

    def create_summary_data(self):
        if len(self.build_summary()) > 0:
            return ClientSyncSummary.objects.create(
                name='ranaka',
                data=self.build_summary())
