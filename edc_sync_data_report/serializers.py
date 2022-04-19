from rest_framework import serializers

from edc_sync_data_report.models import ClientSyncSummary
from edc_sync_data_report.models.sync_confirmation_ids import SyncConfirmationIds


class ClientSyncSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSyncSummary
        fields = ['name', 'data', 'created_date']


class SyncSummarySerializer(serializers.Serializer):

    model_name = serializers.CharField(max_length=255)
    server_value = serializers.CharField(max_length=50)
    client_value = serializers.CharField(max_length=255)
    label = serializers.CharField(max_length=255)
    diff = serializers.CharField(max_length=255)


class SyncConfirmationIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncConfirmationIds
        fields = ['primary_key', 'app_label', 'model_name', 'data_collection_date']
