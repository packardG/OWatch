# OWatch

Web Scraping slash command built for Slack integration.
Currently in the works, and maybe one day will release for public Slack use. For now it is just a custom integration you can add to your own Slack pages. Needs a bit more work then will try and get approved for public Slack use.

This bot gets info from [Master Overwatch](masteroverwatch.com) based on a user input of a Battle.net username.
It prints out an overview of player stats to the slack chat.

After properly setting up a slash command integration on Slack, use this command like so:

/owatch JohnDoe#1693

In its current form, OWatch only works for PC platform lookups in the US region. Soon the option to search within any region, on any platform will come. This is simply a pet project for fun and because I like Overwatch so much.

Libraries used:
- [Flask](http://flask.pocoo.org/)
- [SlackClient](https://github.com/slackapi/python-slackclient)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](http://docs.python-requests.org/en/master/)
