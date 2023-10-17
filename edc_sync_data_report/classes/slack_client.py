from django.conf import settings
from slack import WebClient
from slack.errors import SlackApiError


class SlakClient:
    """
        Send a slack notification to the specified slack channel.
    """

    def send_slack_message(self, message=None):
        client = WebClient(token=settings.SLACK_API_TOKEN)
        try:
            response = client.chat_postMessage(channel='#sync_monitoring', text=message)
            return response
        except SlackApiError as e:
            return {"status": "Failed", "message": f"Got an error: {e.response['error']}"}
