## S&P 500 Twitter Sentiment Scraper

### Scrapes Twitter feeds for sentiment pertaining to all SP500 composites for day-to-day analysis.

### Two seperate queries for each stock are made using Twitter's Tweepy API: one that pertains to tweets that include the specific ticker (e.g. 'AAPL') and the second to tweets that include the name of the company (e.g. 'Apple Inc.').

### Daily updates populate rows of csv chronologically. For example, running daily_update.py EOD on 2018-05-17 may look as follows:

####     ...
#### 2018-05-17 | {'positive_sentiment = 21', 'negative_sentiment = 12', 'neutral_sentiment = 41'}
####     ...
