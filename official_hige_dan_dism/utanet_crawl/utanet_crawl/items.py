# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UtanetCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SongCrawlItem(scrapy.Item):
    title = scrapy.Field()  # 曲のタイトル
    url = scrapy.Field()  # 曲のURL
    lyric = scrapy.Field()  # 歌詞
