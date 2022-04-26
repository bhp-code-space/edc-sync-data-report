from django.db import models
from edc_base.model_mixins import BaseUuidModel

from edc_base.sites import SiteModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base

from edc_sync_data_report.models.sync_site import SyncSite


class SyncAPIsManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        return fields

    class Meta:
        abstract = True
# TODO: review if this model is required

class SyncAPIs(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    # identifier_cls = ExportIdentifier

    sync_site = models.ForeignKey(SyncSite,
                               on_delete=models.CASCADE)

    name = models.CharField(
        verbose_name="Name of API",
        max_length=36)

    uri = models.CharField(
        verbose_name="URI",
        max_length=36,
        unique=True,
        editable=False)

    http_method = models.CharField(
        max_length=100, blank=True,
        default='HTTP Request Method')

    parameters = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('name')
        return fields

    class Meta:
        app_label = 'edc_sync_data_report'
