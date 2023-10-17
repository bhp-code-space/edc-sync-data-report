from datetime import date, datetime

from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

from edc_sync_data_report.models.sync_confirmation_ids import SyncConfirmationIds
from edc_sync_data_report.serializers import SyncConfirmationIdsSerializer


class SyncConfirmationIdsViewAPI(APIView):
    template_name = 'data_summary_report.html'

    def get(self, request, format=None, created_date=None, site_id=None):
        created_date = datetime.strptime(created_date, '%Y-%m-%d')

        data = SyncConfirmationIds.objects.filter(
            created_date=created_date.date() or date.today(),
            site__id=site_id or settings.SITE_ID)
        serializer = SyncConfirmationIdsSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
