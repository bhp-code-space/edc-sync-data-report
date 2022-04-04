from edc_sync_data_report.models import SyncModels
from django.apps import apps
from django.conf import settings


class SummaryData:

    def count_by_app_label_and_model_name(self, app_label, model_name, site_id):
        model_cls = apps.get_model(app_label, model_name)
        return model_cls.objects.filter(site__site_id=site_id).count()

    def build_summary(self, site_id=None):
        data = {}
        sync_models = SyncModels.objects.filter(site__site_id=site_id)

        for sync_model in sync_models:
            key = f'{sync_model.app_label}__{sync_model.model_name}'
            model_data = {f'{key}': self.count_by_app_label_and_model_name(
                sync_model.app_label, sync_model.model_name, site_id=site_id or settings.SITE_ID)}
            data.update(model_data)
        return data
