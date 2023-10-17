from unittest.mock import MagicMock, patch

from django.test import TestCase

from edc_sync_data_report.classes.notification import Notification


class BuildMethodTestCase(TestCase):

    @patch('edc_sync_data_report.classes.notification.SyncSite.objects.filter')
    def setUp(self, mock_filter):
        site_object = MagicMock()
        site_object.server = 'mysite.com'
        site_object.site_id = 'site_1'
        site_object.name = 'MySite'
        mock_filter.return_value = [site_object]
        self.notification = Notification()

    @patch.object(Notification, "build_all_sites_report")
    @patch.object(Notification, "send")
    def test_build_when_no_data(self, mock_send, mock_build_all_sites_report):
        mock_build_all_sites_report.return_value = []

        self.notification.build()

        mock_send.assert_called_once_with(subject="EDC Synchronization Report",
                                          template_body_name="message_noreport.html")
