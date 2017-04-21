def getOffer():
	fo = open('offers.txt', 'r')
	data = fo.read()
	data = data.split(',')
	return data

def getSale(preferences):
	fo = open('sale.txt', 'r')
	data = fo.read()
	data = data.split(',')
	k = []
	for i in preferences:
		if i in data:
			k.append(i)
	return k