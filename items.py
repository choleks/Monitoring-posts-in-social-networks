from scrapy import Item, Field


class TweetItem(Item):
    text = Field()
    keyword = Field()
    account = Field()
