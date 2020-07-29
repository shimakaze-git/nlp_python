import re
import scrapy
from utanet_crawl.items import SongCrawlItem

from bs4 import BeautifulSoup


class HigeDanSpider(scrapy.Spider):
    name = 'hige_dan'
    allowed_domains = ['www.uta-net.com']
    start_urls = ['http://www.uta-net.com/artist/18093']

    def parse(self, response):

        # 髭男dismのアーティストID
        for song in response.css('tbody').css('tr'):
            item = SongCrawlItem()

            song_title = song.css('td.td1 a::text').extract_first()
            song_path = song.css('td.td1 a::attr(href)').extract_first()

            item['title'] = song_title
            song_url = 'http://' + self.allowed_domains[0] + song_path

            yield scrapy.Request(
                song_url,
                callback=self.parse_lyrics,
                meta={'item': item}
            )

    def parse_lyrics(self, response):
        # 歌詞自体を抽出する
        item = response.meta['item']
        item['url'] = response.url

        # text
        text = response.css('div#kashi_area').extract_first()
        soup = BeautifulSoup(text, 'html')
        soup = soup.find('div', itemprop='text')
        song_lyrics = soup.getText()

        # テキストのクリーニング
        song_lyrics = self.text_cleaning(song_lyrics)

        # 歌詞
        item['lyric'] = song_lyrics

        yield item

    def text_cleaning(self, text):
        song_lyrics = text.replace('\n', '')
        song_lyrics = song_lyrics.replace('　', '')

        # 英数字の排除
        song_lyrics = re.sub(r'[a-zA-Z0-9]', '', song_lyrics)
        # 記号の排除
        song_lyrics = re.sub(
            r'[ ＜＞♪`‘’“”・…_！？!-/:-@[-`{-~]', '', song_lyrics
        )

        # 注意書きの排除
        song_lyrics = re.sub(r'注意：.+', '', song_lyrics)

        return song_lyrics
