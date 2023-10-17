from django.test import TestCase

from edc_sync_data_report.classes import ReportSummaryData
from edc_sync_data_report.classes.row_data import RowData


class ReportSummaryDataTest(TestCase):

    def setUp(self):
        self.server_data = {
            'model1': 3,
            'model2': 2,
            'model3': 0,  # <-- data is not matching
        }
        self.client_data = {
            'model1': 3,
            'model2': 2,
            'model3': 1,  # <-- data is not matching
        }
        self.report = ReportSummaryData(server_data=self.server_data,
                                        client_data=self.client_data)

    def test_data_comparison(self):
        matching, not_matching = self.report.data_comparison()
        self.assertIsInstance(matching[0], RowData)
        # added test if not_matching is empty
        self.assertNotEqual(len(not_matching), 0, "List not_matching should not be empty.")
        self.assertIsInstance(not_matching[0], RowData)
        self.assertEqual(not_matching[0].model_name, 'model3')

    def test_is_all_models_matching(self):
        self.assertFalse(self.report.is_all_models_matching())