
from django.db import models


class ClientSyncSummary(models.Model):

    name = models.CharField(max_length=200, null=True)

    data = models.JSONField(null=True)

    created_date = models.DateTimeField(
        verbose_name="Created Date",
        null=True,
        auto_now_add=True,
        blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
