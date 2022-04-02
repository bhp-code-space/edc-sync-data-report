from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from edc_sync_data_report.classes import CollectSummaryData
from edc_sync_data_report.models.client_sync_summary import ClientSyncSummary
from edc_sync_data_report.serializers import ClientSyncSummarySerializer


class ListClientSyncSummaryAPI(APIView):
    """
    View to list all Client Sync Summary in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    def get(self, request, format=None):
        """
        Return a list of all Client Sync Summary: Total count against each model in community server.
        """
        objects = ClientSyncSummary.objects.all()
        serializers = ClientSyncSummarySerializer(objects, many=True)
        return Response(serializers.data)


class GetLiveClientSyncSummaryAPI(APIView):

    def get(self, request, format=None):
        """
        Returns a live summary count for each model as of now
        """
        return JsonResponse(CollectSummaryData().build_summary())
