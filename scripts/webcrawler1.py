import scrapy
import re

offer_file_name = "/var/www/html/server/scripts/offers.txt"
sale_file_name = "/var/www/html/server/scripts/sale.txt"

class AbercrombieSpider(scrapy.Spider):
	name = "abercrombie"
	start_urls = ['https://www.abercrombie.com/shop/us/sale']

	def parse(self, response):
		heading = response.css('h4::text').extract()
		a = response.css('a::text').extract()
		fo = open(offer_file_name, 'a')
		f1 = open(sale_file_name, 'a')
		for i in heading:
			i = i.strip()
			i = i.replace('\n', '')
			k = re.search( r'(offer|off|Offer|OFFER|OFF|sale|Sale|SALE)', i, re.M|re.I)
			if k != None:
				if k.group(1) != None:
					fo.write((i+'|Abercrombie,').encode('utf-8'))
		for i in a:
			i = i.strip()
			i = i.replace('\n', '')
			k = re.search( r'(offer|off|Offer|OFFER|OFF|sale|Sale|SALE)', i, re.M|re.I)
			if k != None:
				if k.group(1) != None:
					fo.write((i+'|Abercrombie,').encode('utf-8'))
				else:
					f1.write((i+'|Abercrombie,').encode('utf-8'))
			else:
				if i != '':
					f1.write((i+'|Abercrombie,').encode('utf-8'))
		fo.close()
		f1.close()

		yield {
			'heading': heading,
			'a': a
		}