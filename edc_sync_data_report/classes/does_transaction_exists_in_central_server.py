from django.apps import apps as django_apps

from django.core.exceptions import ObjectDoesNotExist


class DoesTransactionExistsInCentralServer:

    """
        Checks if the record exists in central server given primary key.
    """

    def sync_data_check(self, data):
        missing_records = []
        for record in data:
            model_cls = django_apps.get_model(model_name=record["model_name"], app_label=record["app_label"]) #
            # Fixme handle a case where model does exits
            try:
                obj = model_cls.objects.get(id=record["primary_key"])
            except ObjectDoesNotExist:
                missing_records.append(record)
        return missing_records
