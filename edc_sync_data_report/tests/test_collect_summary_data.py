from django.test import TestCase
from datetime import datetime

from edc_sync_data_report.classes import ClientCollectSummaryData
from edc_sync_data_report.models import SyncModels, SyncStudy, ClientSyncSummary


class CollectSummaryDataTestCase(TestCase):
    def setUp(self):
        SyncModels.objects.create(
            app_label='edc_sync_data_report',
            model_name='SyncStudy',
            valid_from=datetime.now()
        )

    def test_build_summary(self):
        """"""
        collect = ClientCollectSummaryData()

        SyncStudy.objects.create(
            study_name='flourish',
            description='Flourish Study'
        )
        SyncStudy.objects.create(
            study_name='flourish 1',
            description='Flourish Study 1'
        )

        self.assertEqual(len(collect.build_summary()), 1)
        self.assertEqual(collect.build_summary()['edc_sync_data_report__SyncStudy'], 2)

    def test_create_summary_data(self):
        """ """
        collect = ClientCollectSummaryData()

        SyncStudy.objects.create(
            study_name='flourish',
            description='Flourish Study'
        )
        SyncStudy.objects.create(
            study_name='flourish 1',
            description='Flourish Study 1'
        )

        collect.create_summary_data()
        self.assertEqual(1, ClientSyncSummary.objects.count())
