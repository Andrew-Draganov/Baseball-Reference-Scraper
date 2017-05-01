Inspired by andrewblim's br-scraper, this code scrapes baseball-reference.com for information from the 2016 season.  The resulting tables are output in a csv format.

Information scraped includes players, teams, batting, pitching and fielding.  Trades are also accounted for through the player-team-ID table, which stores a list of all teams that a player played for during the 2016 season.

Scraping is done using Beautiful Soup 4.

A problem to consider is that baseball-reference.com has several tables per page that are commented out in the HTML, so you need to use regex commands to remove the comment markers before invoking bs4.
