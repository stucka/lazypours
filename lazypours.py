#!/python27/python
import requests
import re
from pyquery import PyQuery
import time

# To do:
# -- Modularize retrieval of tap info
# -- Split up brewery and brew with regex
# -- Begin looking for changes
# -- Tweet using code lifted from pacer-rss


maxtaps=45
full_url = 'http://admin.lazydoggrowler.com/nowpouring.aspx'
page = PyQuery(open("nowpouring.aspx").read())
#page = PyQuery(full_url)

class beer(object):
	def __init__(self):
		self.name = ""
		self.hometown = ""
		self.abv = 0.0
		self.style = ""
		self.description = ""
		self.link = ""

def main():
	print "Starting program ..."
	global beers
	beers = list()
	x = beer()
	beer.name="blank"
	beers.append(x)
	for tap in range(1,(maxtaps)):
		x = beer()
		x.name = page("td").eq((10*tap)-5).text().strip()
		x.hometown = page("td").eq((10*tap)-4).text().strip()
		x.abv = page("td").eq((10*tap)-3).text().strip()
		x.style = page("td").eq((10*tap)-2).text().strip()
		x.description = page("td").eq((10*tap)-1).text().strip()
		x.links = page("td").eq((10*tap)+2).html()
		beers.append(x)

	for tap in range(1, (maxtaps)):
		print beers[tap].name
	
	return


if __name__ == '__main__':
	main()






