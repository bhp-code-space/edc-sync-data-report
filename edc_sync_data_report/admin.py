from django.contrib import admin
from .models import SyncSite, SyncModels


@admin.register(SyncSite)
class SyncSiteAdmin(admin.ModelAdmin):

    list_display = ('study', 'server', 'name', 'site_id')


@admin.register(SyncModels)
class SyncModelsAdmin(admin.ModelAdmin):
    pass

