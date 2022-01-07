# -*- coding: utf-8 -*-
#!/usr/bin/python
from multiprocessing import Pool
import os, sys, csv, platform, datetime, glob, requests
from scrapy.http import TextResponse

spider_names = {}
def _crawl(spider_name_params=None):
    if spider_name_params:
        print (spider_name_params)
        print (">>>>> Starting {} spider".format(spider_name_params))
        brand = spider_name_params.split('---')[0].replace(' ', '_')
        url = spider_name_params.split('---')[1]
        filepath = brand.replace(' ', '_') + '.csv'
        if os.path.isfile(filepath):
            os.remove(filepath)
        command = "scrapy crawl alkomprar_com_spider -o {} -a brand={} -a url={}".format(filepath, brand, url)

        os.system(command)
        print ("finished.")
    return None

def run_crawler(spider_names):

    for spider_name in spider_names.keys():
        pool = Pool(processes=5)
        data = spider_name+ '---' +spider_names[spider_name]
        pool.map(_crawl, [data])

if __name__ == '__main__':

    html = requests.get('https://print24.com/fr/').text
    response = TextResponse(url='', body=html, encoding='utf-8')

    brand_urls_tag = response.xpath('//div[@id="productmenu"]//li[@item_group]/a')
    for a in brand_urls_tag:
        title = a.xpath('./div/text()').extract_first()
        url = a.xpath('./@href').extract_first()
        # if url == '/fr/product/brochures/' or url == '/fr/':
        if url == '/fr/':
            spider_names[title] = url
    # if len(sys.argv) == 1:
    #     spider_names = ['nastygal_com_spider', 'coolstuffinc_com_spider', 'theoutnet_com_spider', 'trollandtoad_com_spider']
    # elif len(sys.argv) == 2:
    #     spider_names = [sys.argv[1]]
    run_crawler(spider_names)
