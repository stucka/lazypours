#!/usr/bin/python
import requests
import re
from pyquery import PyQuery
import time

# To do:
# -- Split up brewery and brew with regex
# -- Begin looking for changes
# -- Tweet using code lifted from pacer-rss


maxtaps=45
full_url = 'http://admin.lazydoggrowler.com/nowpouring.aspx'
page = PyQuery(open("nowpouring.aspx").read())
#page = PyQuery(full_url)

class beer(object):
	def __init__(self):
		self.fullname = ""
		self.hometown = ""
		self.abv = 0.0
		self.style = ""
		self.description = ""
		self.link = ""

def get_beer(tap, beer):
	beer.fullname = page("td").eq((10*tap)-5).text().strip()
	beer.hometown = page("td").eq((10*tap)-4).text().strip()
	beer.abv = page("td").eq((10*tap)-3).text().strip()
	beer.style = page("td").eq((10*tap)-2).text().strip()
	beer.description = page("td").eq((10*tap)-1).text().strip()
	beer.links = page("td").eq((10*tap)+2).html()
	return tap, beer

def main():
	print "Starting program ..."
	global beers
	beers = list()
	x = beer()
	beer.name="blank"
	beers.append(x)			# Let's just dummy up something for tap 0
	print "Pulling in list of beers ..."
	for tap in range(1,(maxtaps)):
		x = beer()
		get_beer(tap, x)
		beers.append(x)

	for tap in range(1, (maxtaps)):
		print beers[tap].fullname
	
	return


if __name__ == '__main__':
	main()






