from django.db import models
from edc_base.model_mixins import BaseUuidModel

from edc_base.sites import SiteModelMixin


class SyncDataTestModel(SiteModelMixin, BaseUuidModel):

    field1 = models.CharField(
        verbose_name="App label",
        max_length=100, blank=False)

    field2 = models.CharField(
        verbose_name="App label",
        max_length=100, blank=False)

    class Meta:
        app_label = 'edc_sync_data_report'
