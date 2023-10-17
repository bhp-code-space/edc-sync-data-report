from smtplib import SMTPAuthenticationError, SMTPException
from unittest.mock import MagicMock, patch

import requests
from django.template.loader import TemplateDoesNotExist
from django.test import TestCase

from edc_sync_data_report.classes.notification import Notification


class NotificationTestCase(TestCase):

    @patch('edc_sync_data_report.classes.notification.SyncSite.objects.filter')
    def setUp(self, mock_filter):
        mock_filter.return_value = [
            MagicMock(server='mock_server', site_id='site1', name='Site 1')]
        self.notification = Notification()

    @patch('requests.get')
    @patch(
        'edc_sync_data_report.classes.notification.ServerCollectSummaryData'
        '.build_summary')
    def test_build_all_sites_report_exception(self, mock_build_summary, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        mock_build_summary.return_value = {}

        report = self.notification.build_all_sites_report()

        self.assertEqual(report, [])  # Report should be empty on request exception


    @patch('edc_sync_data_report.classes.notification.render_to_string')
    @patch('edc_sync_data_report.classes.notification.EmailMultiAlternatives')
    def test_send(self, mock_email, mock_render):
        mock_render.return_value = 'Rendered string'

        self.notification.send()

        self.assertEqual(mock_email.call_count, 1)
        self.assertEqual(mock_email.return_value.attach_alternative.call_count, 1)

    @patch('edc_sync_data_report.classes.notification.render_to_string')
    def test_send_template_not_found(self, mock_render):
        # Test error handling for non-existent template
        mock_render.side_effect = TemplateDoesNotExist

        self.notification.send()

    @patch('edc_sync_data_report.classes.notification.EmailMultiAlternatives')
    def test_send_smtp_authentication_error(self, mock_email):
        # Test error handling for SMTPAuthenticationError
        mock_email.side_effect = SMTPAuthenticationError

        self.notification.send()

    @patch('edc_sync_data_report.classes.notification.EmailMultiAlternatives')
    def test_send_smtp_exception(self, mock_email):
        # Test error handling for SMTPException
        mock_email.side_effect = SMTPException

        self.notification.send()
