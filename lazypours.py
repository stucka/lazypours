#!/usr/bin/python
import requests
import re
from pyquery import PyQuery
import time

# To do:
# -- Begin looking for changes
# -- Tweet using code lifted from pacer-rss


maxtaps=45
full_url = 'http://admin.lazydoggrowler.com/nowpouring.aspx'
page = PyQuery(open("nowpouring.aspx").read())
#page = PyQuery(full_url)

class beer(object):
	def __init__(self):
		self.fullname = ""
		self.brewery = ""
		self.label = ""
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
	x = beer.fullname.find(':')
	beer.brewery = beer.fullname[0:x-1].strip()
	beer.label = beer.fullname[x+1:].strip()
			# Some of this needs an explanation. The "fullname" is brewery and label together.
			# It might look something like Molson : Canadian Lager. We split on the colon.
			# Below, we're trying to see if RateBeer or BeerAdvocate links are included in the code.
			# If they are, there are a bunch of quote marks that show up. We look for the quote marks.
			# If we've got at least four, then we've got at least one URL, and that's all we can get
			# into Twitter easily, so let's stay with the first one we find, if we find one.
			# These look like this:
			# <a id="BeerRepeater_ctl35_RateBeerURL" 
			# href="http://www.ratebeer.com/beer/abita-andygator/3/" target="_blank"  ....
			# So the first pair of quotes IDs the beer reviewing organization, second gets us the URL.
			# Python indexes start at 0. So the second pair is indices 2 and 3.
	rawlinks = page("td").eq((10*tap)+2).html().strip()
	starts = [match.start() for match in re.finditer(re.escape('"'), rawlinks)]
	if len(starts) >= 4:
		beer.links = rawlinks[starts[2]+1:starts[3]]
	else:
		beer.links = ""
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

#	for tap in range(1, (maxtaps)):
#		print beers[tap].fullname
	
	return


if __name__ == '__main__':
	main()






