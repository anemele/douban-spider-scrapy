# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy import Spider
from scrapy.exporters import CsvItemExporter

from .spiders.config import INFO_PATH


class DoubanPipeline:
    def __init__(self) -> None:
        self.file = open(INFO_PATH, 'wb')
        self.exporter = CsvItemExporter(self.file, False)
        self.exporter.start_exporting()

    def close_spider(self, spider: Spider):
        self.exporter.finish_exporting()
        self.file.close()
        spider.logger.info(f'Close file {self.file.name}')

    def process_item(self, item, spider):
        # Switch choice
        msg_type = item.pop('type')

        if msg_type == 'info':
            self.exporter.export_item(item)
            return f'save info {item.get("name")}'

        elif msg_type == 'image':
            item.get('img-save-path').write_bytes(item.get('bytes'))
            return f'saved picture {item.get("film-name")} at {item.get("img-name")}'

        return ''
