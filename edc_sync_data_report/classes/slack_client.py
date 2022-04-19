from slack import WebClient
from slack.errors import SlackApiError

from django.conf import settings


class SlakClient:

    def send_slack_message(self, message=None):
        client = WebClient(token=settings.SLACK_API_TOKEN)
        try:
            response = client.chat_postMessage(
                channel='#sync_monitoring',
                text=message)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
