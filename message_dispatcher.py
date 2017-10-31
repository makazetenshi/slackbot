import os
from slackclient import SlackClient
class MessageDispatcher:
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

    @staticmethod
    def dispatch_message(channel, message, slack_client):
        slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)

if __name__ == "__main__":
    main()
