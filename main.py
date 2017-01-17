import os
import requests
from flask import Flask, request, Response
from bs4 import BeautifulSoup

import app as bot

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

help_msg = 'This slash command is used to return stats from an Overwatch player profile.\n \
Correct usage example:  /owatch JohnDoe#0420.\n \
Currently this tool only supports lookups for US PC players, additional support coming soon!'


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_TOKEN:
        channel = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        text = request.form.get('text')
        userID = handleInput(text)
        if userID == None:
            bot.send_message(channel_id, help_msg)
            return Response(), 200
        else:
            soup = scrape(userID)
            # Check here for qp, comp, region, platform, etc.
            headerStats, overallStats_qp, favHeroes_qp = compileStats(soup)
            bot.send_headerStats(channel_id, '#'.join(userID), headerStats)
            bot.send_overallStats(channel_id, overallStats_qp)
            bot.send_favHeroes(channel_id, favHeroes_qp)
            inbound_message = username + " in " + channel + " says: " + text
            print(inbound_message)
    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


def handleInput(text):
    if len(text) == 0:
        print 'No input'
        return None
    args = text.split()
    if args[0] == 'help':
        print 'help me!'
        return None
    else:
        userID = args[0].split('#', 1)
        num_args = len(args)
        return userID


def scrape(userID):
    page = requests.get(
        "https://masteroverwatch.com/profile/pc/us/{}-{}".format(userID[0], userID[1]))
    data = page.content
    soup = BeautifulSoup(data)
    return soup

def compileStats(soup):
    # Tried to implement with a dictionary, wouldve been cleaner.
    # Will continue fiddling to clean it up with a dict or other structure
    headerStats = []
    overallStats_comp = []
    overallStats_qp = []
    favHeroes_comp = []
    favHeroes_qp = []

    # Grabbing the quick play header stats (player overview)
    samples_0 = soup.find_all('div', 'header-stat')
    for i in samples_0:
        temp = i.find('strong').get_text()
        headerStats.append(temp.strip())
    # Hackjob way of isolating the SR better. Works, but ugly.
    sr = headerStats[0].split()
    headerStats[0] = sr

    # Grabbing the overall stats for quick play
    samples_1 = soup.find_all('strong', 'stats-value')
    for i in samples_1:
        temp = i.get_text()
        overallStats_qp.append(temp.strip())

    # Grabbing all the favorite hero stats for quick play
    samples_2 = soup.find_all('div', 'summary-row-container')
    for i in samples_2:
        hero = i.find('span', 'summary-hero-name').get_text()
        kd = i.find('div', 'summary-stats-kda').get_text()
        t = i.find('div', 'summary-winrate col-xs-3')
        winp = t.find_next('strong').get_text()
        #winp = i.find('strong', 'stats-assists')
        temp = [hero, kd, winp]
        favHeroes_qp.append(temp)

    return headerStats, overallStats_qp, favHeroes_qp

if __name__ == '__main__':
    app.run(debug=True)
