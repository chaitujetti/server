import scrapy
import re

class OffersSpider(scrapy.Spider):
	name = "Offers"
	start_urls = ['http://www.calvinklein.us/shop/en/ck/sale']

	def parse(self, response):
		title = response.css('title::text').extract()
		heading = response.css('h2::text').extract()
		passage = response.css('p::text').extract()
		a = response.css('a::text').extract()
		fo = open('offers.txt', 'w')
		f1 = open('sale.txt', 'w')
		for i in title:
			i = i.strip()
			i = i.replace('\n', '')
			k = re.search( r'(offer|off|Offer|OFFER|OFF|sale|Sale|SALE)', i, re.M|re.I)
			if k != None:
				if k.group(1) != None:
					fo.write((i+'|Calvin Klein,').encode('utf-8'))
		for i in heading:
			i = i.strip()
			i = i.replace('\n', '')
			k = re.search( r'(offer|off|Offer|OFFER|OFF|sale|Sale|SALE)', i, re.M|re.I)
			if k != None:
				if k.group(1) != None:
					fo.write((i+'|Calvin Klein,').encode('utf-8'))
		for i in passage:
			i = i.strip()
			i = i.replace('\n', '')
			k = re.search( r'(offer|off|Offer|OFFER|OFF|sale|Sale|SALE)', i, re.M|re.I)
			if k != None:
				if k.group(1) != None:
					fo.write((i+'|Calvin Klein,').encode('utf-8'))
		for i in a:
			i = i.strip()
			i = i.replace('\n', '')
			k = re.search( r'(offer|off|Offer|OFFER|OFF|sale|Sale|SALE)', i, re.M|re.I)
			if k != None:
				if k.group(1) != None:
					fo.write((i+'|Calvin Klein,').encode('utf-8'))
				else:
					f1.write((i+'|Calvin Klein,').encode('utf-8'))
			else:
				if i != '':
					f1.write((i+'|Abercrombie,').encode('utf-8'))
		fo.close()
		f1.close()

		yield {
			'title': title,
			'heading': heading,
			'passage': passage,
			'a': a
		}


