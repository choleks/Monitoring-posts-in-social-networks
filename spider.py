from scrapy import Spider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from re import sub, search
from items import TweetItem


settings = {
    'ROBOTSTXT_OBEY': True,
    'LOG_FILE': 'main.log',
    'ITEM_PIPELINES': {'pipelines.ScraperPipeline': 300}
}


class ScraperSpider(Spider):
    """Twitter scraper
    """
    name = 'spider'
    allowed_domains = 'twitter.com',
    start_urls = 'https://mobile.twitter.com',

    def __init__(self, accounts, keywords, tweet_min_length=20, *args, **kwargs):
        """accounts: TWAccount model queryset
        keywords: Keyword model queryset
        """
        super().__init__(*args, **kwargs)
        self.accounts = accounts
        self.keywords = keywords
        self.tweet_min_length = tweet_min_length

    def parse(self, _response):
        for account in self.accounts:
            yield Request('https://mobile.twitter.com/{0}'.format(account), callback=self.parse_tweets)

    def parse_tweets(self, response):
        current_account = response.url[response.url.rfind('/') + 1:]

        for tweet_div in response.xpath('//div[@class="dir-ltr"]'):
            text = sub(r'[^a-zа-я0-9іїй ]', '', ''.join(tweet_div.xpath('text()').getall()).lower())

            if text is None:
                continue

            keyword = self.search_for_keywords(text)

            if keyword is None:
                continue

            tweet = TweetItem()
            tweet['text'] = text
            tweet['keyword'] = keyword
            tweet['account'] = current_account
            yield tweet

    def search_for_keywords(self, text):
        for keyword in self.keywords:
            if search(keyword, text) is not None:
                return keyword


def run_spider(accounts, keywords):
    """Start scraping
    """
    process = CrawlerProcess(settings)
    process.crawl(ScraperSpider, accounts=accounts, keywords=keywords)
    process.start()


run_spider(['vesti_news'], ['нато', 'росс'])
