from django.db import models
from edc_base.model_mixins import BaseUuidModel

from edc_base.sites import SiteModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base


class SyncSiteManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        return fields

    class Meta:
        abstract = True


class SyncModels(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    app_label = models.CharField(
        verbose_name="App label",
        max_length=100, blank=False)

    model_name = models.CharField(
        verbose_name="class reference absolute path",
        max_length=200, blank=False)

    description = models.CharField(max_length=255, blank=True)

    valid_from = models.DateField(
        verbose_name="Report start date",
        null=True,
        blank=True)

    valid_to = models.DateField(
        verbose_name="Report start date",
        null=True,
        blank=True)

    def __str__(self):
        return f'{self.model_name}'

    def natural_key(self):
        return self.model_name

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('model_name')
        return fields

    class Meta:
        app_label = 'edc_sync_data_report'
