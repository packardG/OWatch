import os
from slackclient import SlackClient

SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

sc = SlackClient(SLACK_API_KEY)


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


# Need to check what type of channel it comes from first.
# So if from DM, send back to DM,, if pvt group, send back to that.
# and else if a public channel, send normally back.

def send_message(channel_id, message):
    sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        response_type='in_channel',
        text=message,
        username='OWatch',
        icon_emoji=':zap:'
    )


def send_headerStats(channel_id, user, stats):
    sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        response_type='in_channel',
        text=user + '\n*Summary:*\n\n' +
        '*SR:* ' + stats[0][0] +
        '\n*Percentile:* ' + stats[0][1] +
        '\n*Regional Rank:* ' + stats[1] +
        '\n*W-L-T:* ' + stats[2] +
        '\n*Win Percent:* ' + stats[3] + '\n',
        mrkdwn='true',
        username='OWatch',
        icon_emoji=':zap:'
    )


def send_overallStats(channel_id, stats):
    sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        response_type='in_channel',
        text='*Overall Stats(qp):*\n' +
        '_All stats are avgs per minute_\n\n' +
        '*Elims:* ' + stats[0] +
        '\n*K/D:* ' + stats[1] +
        '\n*Dmg:* ' + stats[2] +
        '\n*Blocked:* ' + stats[3] +
        '\n*Healing:* ' + stats[4] +
        '\n*Medals:* ' + stats[5] + '\n',
        mrkdwn='true',
        username='OWatch',
        icon_emoji=':zap:'
    )


def send_favHeroes(channel_id, stats):
    sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        response_type='in_channel',
        text='*Favorite Heroes:*\n\n' +
        stats[0][0] + ': \n' + stats[0][1] + '\n' + stats[0][2] + '  Winrate\n' +
        stats[1][0] + ': \n' + stats[1][1] + '\n' + stats[1][2] + '  Winrate\n' +
        stats[2][0] + ': \n' + stats[2][1] + '\n' + stats[2][2] + '  Winrate\n',
        mrkdwn='true',
        username='OWatch',
        icon_emoji=':zap:'
    )


def main():
    print 'Hey from main!'

if __name__ == '__main__':
    main()
