import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

sc = SlackClient(SLACK_TOKEN)


def list_channels():
    channels_call = sc.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None

def channel_info(channel_id):
    sc.api_call(
        "channels.info",
        channel=channel_id,
    )

def send_message(channel_id, message):
    sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='OWatch',
        icon_emoji=':robot_face:'
    )

def main():
    print 'Hey from main!'

if __name__ == '__main__':
    main()
