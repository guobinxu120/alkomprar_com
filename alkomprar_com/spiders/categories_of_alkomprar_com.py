import scrapy
# from urlparse import urlparse
from scrapy import Request
from scrapy.utils.response import open_in_browser
from collections import OrderedDict

class CategoriesOfalkomprar_com(scrapy.Spider):

	name = "categories_of_alkomprar_com"
	start_urls = ('https://www.alkomprar.com/',)

	use_selenium = False
	def parse(self, response):
		categories = response.xpath('//ul[@class="menu-content-column-container"]/li/a/@href').extract()

		# yield {'links':list(urlparse(x).path for x in categories)}

	# start_urls = ('https://www.ylighting.com/brands/',)
	# def parse(self, response):
	# 	brand_urls_tag = response.xpath('//*[@class="letterContainer"]/div/ul/li/a')
	# 	previouss = ['Blu Dot', 'Herman Miller', 'Knoll', 'LBL Lighting', 'TECH Lighting', 'Vondom']
	# 	for a in brand_urls_tag:
	# 		title = a.xpath('./@title').extract_first()
	# 		url = a.xpath('./@href').extract_first()
	# 		item = OrderedDict()
	# 		item['brand'] = title
	# 		item['url'] = url
	# 		yield Request(response.urljoin(url), self.final, meta={'item':item})
	# def final(self, response):
	# 	item = response.meta['item']
	# 	total = response.xpath('//div[@class="display-inline-block float-left"]/h4/strong/text()').re(r'[\d]+')
	# 	if total:
	# 		item['total'] = total[-1]
	# 		yield item
	# 	else:
	# 		url = response.xpath('//div[@class="dept-subcat-header"]/a/@href').extract_first()
	# 		yield Request(response.urljoin(url), self.final, response.meta)