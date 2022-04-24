from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.apps import apps

from datetime import date

from edc_sync_data_report.models import SyncModels


class Command(BaseCommand):
    help = 'Delete sync models given app_label'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app_label',
            action='append',
            type=str
        )

        parser.add_argument(
            '--model_name',
            action='append',
            type=str
        )

    def handle(self, *args, **options):
        if len(options.get("app_label")) > 0 and options.get("model_name") is None:
            app_label = options.get("app_label")[0]
            models_to_delete = SyncModels.objects.filter(app_label=app_label)
            models_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(
                ' Deleted all registered sync models for app: "'.format(app_label), ))
        elif len(options.get("app_label")) > 0 and options.get("model_name"):
            app_label = options.get("app_label")[0]
            model_name = options.get("model_name")[0]
            try:
                obj = SyncModels.objects.get(app_label=app_label, model_name=model_name)
                obj.delete()
                self.stdout.write(self.style.SUCCESS(
                    'Deleted model: {} for app: {}."'.format(model_name, app_label)))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.NOTICE(
                    ' Model not registered for synchronization tracking."'.format(model_name), ))
