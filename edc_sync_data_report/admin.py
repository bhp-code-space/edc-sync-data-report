from django.contrib import admin
from .models import SyncSite, SyncModels


@admin.register(SyncSite)
class SyncSiteAdmin(admin.ModelAdmin):
    pass


@admin.register(SyncModels)
class SyncModelsAdmin(admin.ModelAdmin):
    pass

