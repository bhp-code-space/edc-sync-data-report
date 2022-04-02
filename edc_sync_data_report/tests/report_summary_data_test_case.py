from django.test import TestCase

from edc_sync_data_report.classes import ReportSummaryData


class ReportSummaryDataTestCase(TestCase):

    def test_data_comparison(self):
        """"""
        report = ReportSummaryData(
            server_data={'model_a': 1, 'model_b': 3}, client_data={'model_a': 1, 'model_b': 2, 'model_c': 10})
        matching, not_matching = report.data_comparison()
        key = 'model_b'
        exists = False
        for data in not_matching:
            if key in data:
                exists = True
        self.assertTrue(exists)
