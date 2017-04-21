import scrapy

class OffersSpider(scrapy.Spider):
	name = "Offers"
	start_urls = ['http://www.calvinklein.us/shop/en/ck/sale']

	def parse(self, response):
		title = response.css('title::text').extract()
		heading = response.css('h2::text').extract()
		passage = response.css('p::text').extract()
		a = response.css('a::text').extract()
		fo = open('offers.txt', 'w')
		for i in title:
			i = i.replace('\t', '')
			i = i.replace('\n', '')
			if i != '':
				fo.write((i+',').encode('utf-8'))
		for i in heading:
			i = i.replace('\t', '')
			i = i.replace('\n', '')
			if i != '':
				fo.write((i+',').encode('utf-8'))
		for i in passage:
			i = i.replace('\t', '')
			i = i.replace('\n', '')
			if i != '':
				fo.write((i+',').encode('utf-8'))
		fo.close()
		fo = open('sale.txt', 'w')
		for i in a:
			i = i.replace('\t', '')
			i = i.replace('\n', '')
			if i != '':
				fo.write((i+',').encode('utf-8'))
		fo.close()

		yield {
			'title': title,
			'heading': heading,
			'passage': passage,
			'a': a
		}
