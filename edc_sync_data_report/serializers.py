from rest_framework import serializers

from edc_sync_data_report.models import ClientSyncSummary


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