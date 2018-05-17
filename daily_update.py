"""
The script that will update the SPX_sentiment.csv file based on today's date
"""

import requests
import bs4 as bs
import pickle
import datetime
import pandas as pd
import warnings

from twitter_scraper_api import SPX_Twitter_Scraper


class Daily_Update(object):

    def __init__(self):
        self.today = datetime.datetime.now().date()
        self.csv_path = 'C:\\Users\\PeterKokalov\\lpthw\\SUMMER2018\\Twitter_SPX_sentiment\\SPX_sentiment.csv'


    def wiki_scrape(self):
        r = requests.get(
            'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            )
        soup = bs.BeautifulSoup(r.text, 'lxml')
        SP500 = soup.find(
            'table',
            {
                'class': 'wikitable sortable'
                }
            )
        tickers = []; full_names = []
        for ticker in SP500.find_all('tr')[1:]:
            tickers.append(ticker.find_all('td')[0].text)
            full_names.append(ticker.find_all('td')[1].text)

        with open('SP500tickers.pickle', 'wb') as f:
            pickle.dump(tickers, f)

        with open('SP500names.pickle', 'wb') as f:
            pickle.dump(full_names, f)

        return tickers


    def compile_pandas_dataframe(self, update):
        if update:
            tickers = self.wiki_scrape()
        else:
            with open('SP500tickers.pickle', 'rb') as f:
                tickers = pickle.load(f)

        todays_date = datetime.datetime.now().date()
        index = pd.date_range(todays_date + datetime.timedelta(), periods=300, freq='D')
        columns = tickers

        df_ = pd.DataFrame(index=index, columns=columns)
        df_ = df_.fillna(0)

        try:
            df_.to_csv(path_or_buf=self.csv_path)
            print("csv safed successfully")

        except Exception as e:
            print(e)


    def ticker_sentiment(self, day):
        with open('SP500tickers.pickle', 'rb') as t:
            tickers = pickle.load(t)

        with open('SP500names.pickle', 'rb') as n:
            company_names = pickle.load(n)

        df = pd.read_csv(self.csv_path, index_col=[0])
        df.index = pd.to_datetime(df.index)
        api = SPX_Twitter_Scraper()

        warnings.filterwarnings('ignore')
        for tick, name in zip(tickers, company_names):
            df_entry = {
                'positive_tweets': 0,
                'negative_tweets': 0,
                'neutral_tweets': 0
                }
            tick_sentiment = api.return_percentages(tick)
            name_sentiment = api.return_percentages(name)
            if tick_sentiment == 0:
                pass
            else:
                df_entry['positive_tweets'] += tick_sentiment[0]
                df_entry['negative_tweets'] += tick_sentiment[1]
                df_entry['neutral_tweets'] += tick_sentiment[2]
            if name_sentiment == 0:
                pass
            else:
                df_entry['positive_tweets'] += name_sentiment[0]
                df_entry['negative_tweets'] += name_sentiment[1]
                df_entry['neutral_tweets'] += name_sentiment[2]

            df.loc[day, tick] = [df_entry]
        df.to_csv(self.csv_path)


def main():
    Daily_Update_api = Daily_Update()
    # Daily_Update_api.wiki_scrape()
    # Daily_Update_api.compile_pandas_dataframe(update=False)
    Daily_Update_api.ticker_sentiment(Daily_Update_api.today)


if __name__ == "__main__":
    main()
