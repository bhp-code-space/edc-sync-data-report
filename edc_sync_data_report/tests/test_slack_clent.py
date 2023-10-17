from unittest.mock import patch

from django.test import TestCase

from edc_sync_data_report.classes.slack_client import SlakClient


class MockClient:
    def chat_postMessage(self, channel, text):
        if "error" in text:
            return {"status": "Failed", "message": "Test error message"}
        else:
            return {"status": "Success", "message": "Message posted successfully."}


class TestSlackClient(TestCase):
    @patch("edc_sync_data_report.classes.slack_client.WebClient", return_value=MockClient())
    def test_send_slack_message_success(self, mock_web_client):
        slak_client = SlakClient()
        result = slak_client.send_slack_message(message="Hello, World!")
        self.assertEqual(result["status"], "Success")

    @patch("edc_sync_data_report.classes.slack_client.WebClient", return_value=MockClient())
    def test_send_slack_message_failure(self, mock_web_client):
        slak_client = SlakClient()
        result = slak_client.send_slack_message(message="Hello, error here")
        self.assertEqual(result["status"], "Failed")
