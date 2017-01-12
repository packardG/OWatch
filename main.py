import webapp2
from lxml import html
import requests
from bs4 import BeautifulSoup


class OWatch(webapp2.RequestHandler):

    def get(self):
        userID = self.request.get('text')
        scrape(userID, self)


def scrape(userID, self):
    if userID == 'help':
        self.response.write(
            'This slash command is used to return stats from an Overwatch player profile.\n \
Correct usage example:  /owatch JohnDoe#0420.\n \
Currently this tool only supports lookups for US PC players, additional support coming soon!')
    else:
        bnet = userID.split('#', 1)
        page = requests.get(
            'http://masteroverwatch.com/profile/pc/us/{}-{}'.format(bnet[0], bnet[1]))
        data = page.content
        soup = BeautifulSoup(data)
        headerStats, overallStats_comp, overallStats_qp, favHeroes_comp, favHeroes_qp = compileStats(
            soup)
        self.response.write('{}\n'.format(userID))
        self.response.write('-----------------------------------------\n')
        self.response.write('Player Overview\n\n')
        self.response.write('SR:\t {}\n'.format(headerStats[0][0]))
        self.response.write(
            'Player is in the {} percentile\n'.format(headerStats[0][1]))
        self.response.write('US Ranking:\t {}\n'.format(headerStats[1]))
        self.response.write('W-L-T:\t {}\n'.format(headerStats[2]))
        self.response.write('Overall Winrate:\t {}\n'.format(headerStats[3]))
        self.response.write('-----------------------------------------\n')
        self.response.write('Overall Stats\n')
        self.response.write('All stats are avgs per min.\n\n')
        self.response.write('Elims:\t {}\n'.format(overallStats_qp[0]))
        self.response.write('K/D:\t {}\n'.format(overallStats_qp[1]))
        self.response.write('Damage:\t {}\n'.format(overallStats_qp[2]))
        self.response.write('Blocked:\t {}\n'.format(overallStats_qp[3]))
        self.response.write('Healing:\t {}\n'.format(overallStats_qp[4]))
        self.response.write('Medals:\t {}\n'.format(overallStats_qp[5]))
        self.response.write('-----------------------------------------\n')
        self.response.write('Favorite Heroes\n\n')
        self.response.write('{}:\n'.format(favHeroes_qp[0][0]))
        self.response.write('{}\n'.format(favHeroes_qp[0][1]))
        self.response.write('Character winrate: {}\n\n'.format(favHeroes_qp[0][2]))
        self.response.write('{}\n'.format(favHeroes_qp[1][0]))
        self.response.write('{}\n'.format(favHeroes_qp[1][1]))
        self.response.write('Character winrate: {}\n\n'.format(favHeroes_qp[1][2]))
        self.response.write('{}\n'.format(favHeroes_qp[2][0]))
        self.response.write('{}\n'.format(favHeroes_qp[2][1]))
        self.response.write('Character winrate: {}\n'.format(favHeroes_qp[2][2]))
        self.response.write('-----------------------------------------\n')

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

    return headerStats, overallStats_comp, overallStats_qp, favHeroes_comp, favHeroes_qp

app = webapp2.WSGIApplication([
    (r'/', OWatch),
    (r'/owatch', OWatch)
])


def main():
    from paste import httpserver
    httpserver.serve(app, host='localhost', port='8080')

if __name__ == '__main__':
    main()
