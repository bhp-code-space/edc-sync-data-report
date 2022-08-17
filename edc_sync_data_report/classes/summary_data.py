from datetime import date

from django.apps import apps
from django.conf import settings
from django.db import IntegrityError

from edc_sync_data_report.models import SyncModels
from edc_sync_data_report.models.sync_confirmation_ids import SyncConfirmationIds


class SummaryData:
    """
        Based on sync models register, creates a summary report.
    """

    def get_model_by_app_label_and_model_name(self, app_label, model_name, site_id, created_date):
        model_cls = apps.get_model(app_label, model_name)
        # Condition whether it is history or not
        try:
            model_cls.history.model
            return model_cls.objects.filter(
                site__id=site_id, created__date=created_date).values_list('history_id', 'created')
        except AttributeError:
            return model_cls.objects.filter(
                site__id=site_id, created__date=created_date).values_list('id', 'created')

    def count_by_app_label_and_model_name(self, app_label, model_name, site_id):
        model_cls = apps.get_model(app_label, model_name)
        return model_cls.objects.filter(site__site_id=site_id).count()

    def build_summary(self, site_id=None):
        data = {}
        sync_models = SyncModels.objects.filter(site__id=site_id)

        for sync_model in sync_models:
            key = f'{sync_model.app_label}__{sync_model.model_name}'
            model_data = {f'{key}': self.count_by_app_label_and_model_name(
                sync_model.app_label, sync_model.model_name, site_id=site_id or settings.SITE_ID)}
            data.update(model_data)
        return data

    def collect_primary_key_and_save(self, site_id=None, created_date=None):
        """
        Based on Sync models registered list, this method generates values list (id, created) for each model.
        And also, creates a sync confirmation record.
        :param site_id:
        :param created_date:
        :return:
        """
        data = []
        sync_models = SyncModels.objects.filter(site_id=site_id)  # Get registered models

        for sync_model in sync_models:
            values_list = self.get_model_by_app_label_and_model_name(
                sync_model.app_label, sync_model.model_name, site_id=site_id or settings.SITE_ID,
                created_date=created_date)
            for model_obj in values_list:
                model_obj_id, model_obj_created = model_obj
                # Condition whether it is history or not
                try:
                    obj = SyncConfirmationIds.objects.create(
                        app_label=sync_model.app_label,
                        model_name=sync_model.model_name,
                        site_id=site_id,
                        data_collection_date=model_obj_created,
                        primary_key=model_obj_id.hex,
                        created_date=date.today()
                    )
                    data.append(obj)
                except IntegrityError:
                    # already registered key
                    pass


        return data
