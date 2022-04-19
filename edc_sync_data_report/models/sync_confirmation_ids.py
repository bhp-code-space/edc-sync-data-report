from django.db import models
from edc_base.model_mixins import BaseUuidModel

from edc_base.sites import SiteModelMixin


class SyncConfirmationIds(SiteModelMixin, BaseUuidModel):

    primary_key = models.CharField(
        unique=True,
        verbose_name="Model object id",
        max_length=100, blank=False)

    app_label = models.CharField(
        verbose_name="App label",
        max_length=100, blank=False)

    model_name = models.CharField(
        verbose_name="Model Name",
        max_length=200, blank=False)

    created_date = models.DateField(
        verbose_name="Ceated date",
        null=True,
        blank=True)

    data_collection_date = models.DateField(
        verbose_name="Data collection date",
        null=True,
        blank=True)

    is_synced = models.BooleanField(
        null=True,
        blank=True)

    # site_id = models.IntegerField(null=True, blank=True)
