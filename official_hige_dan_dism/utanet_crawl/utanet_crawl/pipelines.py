# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from itemadapter import ItemAdapter


class UtanetCrawlPipeline:

    def open_spider(self, spider):
        write_path = 'lyrics.txt'
        self.file = open(write_path, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = item['lyric'] + '\n'
        self.file.write(line)
        print(line)
        print('----' * 20)
        return item
