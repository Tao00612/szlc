import scrapy
from copy import deepcopy
from szlc.items import SzlcItem
import math
import json


class SzSpider(scrapy.Spider):
    name = 'sz'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.szlcsc.com/index.html']

    def parse(self, response, **kwargs):
        li_list = response.xpath('//div[@class="layout-catalogs ass "]/ul/li')
        for li in li_list:
            s_cate_list = li.xpath('./div/dl/dd')
            for s_cate in s_cate_list[2:3]:
                item = SzlcItem()
                item['b_cate'] = li.xpath('./a/text()').extract_first()
                item['s_cate'] = s_cate.xpath('./a/text()').extract_first()
                item['s_cate_url'] = s_cate.xpath('./a/@href').extract_first()
                cate_id = item['s_cate_url'].split("log/")[-1].split(".ht")[0]
                data = {
                        'catalogNodeId': cate_id,
                        'pageNumber': '1',
                        'querySortBySign': '0',
                        'showOutSockProduct': '1',
                        'showDiscountProduct': '1',
                    }
                item['data'] = data
                yield scrapy.FormRequest(
                    url='https://list.szlcsc.com/products/list',
                    formdata=data,
                    callback=self.parse_detail_product,
                    meta={"item": deepcopy(item)}
                )

    def parse_detail_product(self, response):
        item = deepcopy(response.meta['item'])
        json_dict = response.json()
        content_list = json_dict['productRecordList']
        pagecount = math.ceil(int(json_dict['totalCount']) / 30)
        for content in content_list:
            item['model'] = content['lightProductModel']  # 产品简写
            item['brand'] = content['lightBrandName'] # 品牌名
            item['parameter'] = content['remarkPrefix'] # 参数
            if not item['parameter'] and content['lightProductModel'] != content['lightProductName']:
                item['parameter'] = content['lightProductName']
            item['specifications'] = content['lightStandard'] # 规格
            item['recentlySalesCount'] = content['recentlySalesCount'] # 销量
            yield item
        # 翻页
        page_num = int(item.get('data').get('pageNumber', 0))
        if pagecount > page_num:
            item['data']['pageNumber'] = str(page_num+1)
            print(item['data'])
            yield scrapy.FormRequest(
                url='https://list.szlcsc.com/products/list',
                formdata=item['data'],
                callback=self.parse_detail_product,
                meta={"item": item}
            )


    # def parse_cate_list(self, response):
    #     item = response.meta['item']
    #     table_list = response.xpath('//div[@id="shop-list"]/table')
    #     for table in table_list:
    #         item['model'] = table.xpath('.//div[@class="two-01"]/ul[1]/li[3]/span[2]/text()').extract_first()
    #         item['brand'] = table.xpath('.//div[@class="two-01"]/ul[1]/li[2]/a/text()').extract_first().strip()
    #         item['brand_url'] = table.xpath('.//div[@class="two-01"]/ul[1]/li[2]/a/@href').extract_first()
    #
    #         item['parameter'] = table.xpath('.//span[text()="描述："]/..//text()[2]').extract_first()
    #         if item['parameter']:
    #             item['parameter'] = item['parameter'].strip()
    #         else:
    #             item['parameter'] = '无'
    #
    #         item['specifications'] = table.xpath('.//div[@class="two-01"]/ul/li[1]/span[2]/text()').extract_first()
    #         item['goods_is'] = table.xpath('.//span[text()="有货"]/text()').extract_first()
    #         if not item['goods_is']:
    #             item['goods_is'] = '当前无货'
    #         print(item)
