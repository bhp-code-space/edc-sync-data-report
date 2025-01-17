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


class SyncSite(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    name = models.CharField(max_length=100, blank=True)

    community_site_id = models.CharField(
        verbose_name="Community Site ID",
        max_length=10,
        unique=True,
        editable=False)

    study = models.CharField(
        max_length=100, blank=True,
        default='flourish')

    description = models.CharField(max_length=255, blank=True)

    server = models.CharField(max_length=25,
                              blank=True,
                              help_text="Provide server ip including a port if "
                                        "neccessary. e.g 10.31.31.230:8000")

    valid_from = models.DateField(
        verbose_name="Report start date",
        null=True,
        blank=True)

    valid_to = models.DateField(
        verbose_name="Report start date",
        null=True,
        blank=True)

    def __str__(self):
        return f'{self.community_site_id}'

    def natural_key(self):
        return self.community_site_id

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('community_site_id')
        return fields

    class Meta:
        app_label = 'edc_sync_data_report'
