import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.apps import apps
from edc_base.sites import SiteModelMixin

from datetime import date

from edc_sync_data_report.models import SyncModels

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Registers sync models given app_label'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app_label',
            action='append',
            type=str
        )

        parser.add_argument(
            '--site_id',
            action='append',
            type=int
        )

        parser.add_argument(
            '--model_name',
            action='append',
            type=str
        )

    def handle(self, *args, **options):
        if len(options.get("site_id")) == 0:
            self.stdout.write(self.style.NOTICE(
                'Site ID is mandatory, kindly provide it. e.g --site_id 99'))
        else:
            site = Site.objects.get(id=options.get("site_id")[0])
            if len(options.get("app_label")) > 0 and options.get("model_name") is None:
                app_label = options.get("app_label")[0]
                app_models = apps.get_app_config(app_label).get_models()
                i = 1
                for model in app_models:
                    if issubclass(model, SiteModelMixin):
                        try:
                            SyncModels.objects.get(app_label=app_label, model_name=model._meta.model.__name__)
                            self.stdout.write(self.style.NOTICE(
                                ' {}. {} already registered sync tracking."'.format(i, model._meta.model.__name__), ))
                        except ObjectDoesNotExist:
                            SyncModels.objects.create(
                                app_label=app_label,
                                model_name=model._meta.model.__name__,
                                valid_from=date.today(),
                                site=site
                            )
                            self.stdout.write(self.style.SUCCESS(' {}. {} registered successfully sync tracking."'
                                .format(
                                i, model._meta.model.__name__), ))
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(' {}. {} not registered.  Not a subclass of SiteModelMixin'
                                                             '."'.format(i, model._meta.model.__name__), ))
                    i = i + 1
            elif len(options.get("app_label")) > 0 and options.get("model_name"):
                app_label = options.get("app_label")[0]
                model_name = options.get("model_name")[0]
                try:
                    SyncModels.objects.get(app_label=app_label, model_name=model_name, site__id=options.get("site_id")[0])
                    self.stdout.write(self.style.SUCCESS(
                        '{} already registered sync tracking."'.format(model_name), ))
                except ObjectDoesNotExist:
                    app_label = options.get("app_label")[0]
                    model_name = options.get("model_name")[0]
                    SyncModels.objects.create(
                        app_label=app_label,
                        model_name=model_name,
                        valid_from=date.today(),
                        site=site
                    )
                    logger.info(' {} registered successfully sync tracking."'.format(model_name))
                    self.stdout.write(self.style.SUCCESS(
                        ' {} registered successfully sync tracking."'.format(model_name)))
