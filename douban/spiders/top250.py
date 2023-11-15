from pathlib import Path
from typing import Iterable

import scrapy
from scrapy.http import HtmlResponse, Request

from .config import PIC_PATH


class Top250Spider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['douban.com', 'doubanio.com']
    url = 'https://movie.douban.com/top250?start={}&filter='
    start_urls = []

    def start_requests(self) -> Iterable[Request]:
        # There are 10 pages with 25 films per page
        for page in range(10):
            url = self.url.format(page * 25)
            yield Request(url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        if response.status != 200:
            raise ValueError(f'[ERROR] {response.status}: {response.url}')

        li_list = response.css('ol.grid_view>li')
        for li in li_list:
            # 封面图片 url
            img_src = li.css('img::attr(src)').get()
            if img_src is not None:
                # 高清图片
                img_src = img_src.replace('s_ratio_poster', 'l')
            # 电影名
            film_name = li.css('span.title:first-child::text').get()
            # 电影评分
            rating = li.css('span.rating_num::text').get()
            # 当前评分人数
            people_number = li.css('div.star>span:nth-child(4)::text').get()
            if people_number is not None:
                people_number = people_number[:-3]

            # 包装数据
            yield dict(
                # 辅助信息
                type='info',
                # 电影信息
                name=film_name,
                img_src=img_src,
                rating=rating,
                people_number=people_number,
            )

            if img_src is None:
                continue

            img_name = Path(img_src).name
            img_save_path = PIC_PATH / img_name
            # 若图片存在，则跳过
            if img_save_path.exists():
                continue

            # 保存图片
            img_info = {
                'film-name': film_name,
                'img-name': img_name,
                'img-save-path': img_save_path,
            }
            yield Request(url=img_src, callback=self.parse_image, cb_kwargs=img_info)

    def parse_image(self, response: HtmlResponse, **kwargs):
        # 将请求图片传递到 pipeline
        yield dict(type='image', bytes=response.body, **kwargs)
