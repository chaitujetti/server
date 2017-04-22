
offer_file_name = "/var/www/html/server/scripts/offers.txt"
sale_file_name = "/var/www/html/server/scripts/sale.txt"

def getOffer():
	fo = open(offer_file_name, 'r')
	data = fo.read()
	data = data.split(',')
	return data

def getSale(preferences):
	fo = open(sale_file_name, 'r')
	data = fo.read()
	data = data.split(',')
	k = []
	for i in preferences:
		if i in data:
			k.append(i)
	return k