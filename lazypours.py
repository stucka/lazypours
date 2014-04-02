#!/usr/bin/python
import requests
import re
from pyquery import PyQuery
import time
from twitter import *
import argparse

# To do:
# -- Patch around missing beers that lead to tap number / position in file mismatches
# -- Test code that looks for changes
# -- Tweet using code lifted from pacer-rss


maxtaps=45
full_url = 'http://admin.lazydoggrowler.com/nowpouring.aspx'

houropen=11			# Store opens no earlier than 11 a.m.
hourclose=21		# Store closes no later than 9 p.m.
sleeptime=15*60		# Wait some minutes between checks

#testmode = "n"
#testmode = "y"

class beer(object):
	def __init__(self):
		self.tap = 12345
		self.fullname = ""
		self.brewery = ""
		self.label = ""
		self.hometown = ""
		self.abv = 0.0
		self.style = ""
		self.description = ""
		self.link = ""

def get_beer(slot, beer, pqhandle):
	beer.tap = int(pqhandle("td").eq((10*slot)-6).text().strip()[:-1].strip())
	beer.fullname = pqhandle("td").eq((10*slot)-5).text().strip()
	beer.hometown = pqhandle("td").eq((10*slot)-4).text().strip()
	beer.abv = pqhandle("td").eq((10*slot)-3).text().strip()
	beer.style = pqhandle("td").eq((10*slot)-2).text().strip()
	beer.description = pqhandle("td").eq((10*slot)-1).text().strip()
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
	rawlinks = pqhandle("td").eq((10*slot)+2).html().strip()
	starts = [match.start() for match in re.finditer(re.escape('"'), rawlinks)]
#	print "Tap = " + str(beer.tap) + " : " + beer.label
	if len(starts) >= 4:
		beer.links = rawlinks[starts[2]+1:starts[3]]
	else:
		beer.links = ""
	return slot, beer, pqhandle

def updatecheck():
	page = PyQuery(full_url)
	maxslots = (((page("td").length)-6)/10)+1
	updatelist = list()				# Zero out list.
	x = beer()
	activetaps = 0
	for randomword in range(0,maxtaps+1):
		updatelist.append(x)		# Dummy up a list of empty taps. Keep
									#empty in 0 to keep tap number
									# and index aligned.
	for slot in range(1,maxslots):
		x = beer()
		get_beer(slot, x, page)
		updatelist[x.tap]=x
		activetaps = activetaps + 1
	for tap in range(1,maxtaps):
		if updatelist[tap].fullname != beers[tap].fullname:
			if updatelist[tap].fullname.length <3:
				beers[tap]=updatelist[tap]
				print "Tap " + str(tap) + " has gone dry."
			else:
				beers[tap]=updatelist[tap]
				print "Whoohoo! New beer " + beers[tap].fullname + " on tap " + str(tap)
	print str(activetaps) + " active taps found."

#		if x.fullname == beers[tap].fullname:
#			print "x.fullname: " + x.fullname
#			print "beers[tap]: " + beers[tap].fullname + str(tap)
#			pass			
#		else:
#			print "Whoohoo! New beer on tap " + str(tap) + x.fullname
#			beers[tap] = x
			
	return

def make_notifier(creds, twitter=False):
    """Make a notifier function with access to credentials, etc."""
    def notify(entry):
        if twitter:
            send_tweet(entry, creds['oauth_token'], creds['oauth_secret'],
                       creds['consumer_key'], creds['consumer_secret'] )
    return notify



def main():
	print "Starting program ..."
	# Get command-line arguments.
	parser = argparse.ArgumentParser()
	parser.add_argument("--twitter", action='store_true')
	for arg in ["--e-from", "--e-pass", "--e-to",
			"--t-oauth-token", "--t-oauth-secret",
			"--t-consumer-key", "--t-consumer-secret"]:
		parser.add_argument(arg, action='store', default="")
	args = parser.parse_args()
	notifier = make_notifier(twitter=args.twitter, creds = {
		'oauth_token': args.t_oauth_token,
		'oauth_secret': args.t_oauth_secret,
		'consumer_key': args.t_consumer_key,
		'consumer_secret': args.t_consumer_secret
	})

	global beers
	beers = list()
	x = beer()
	activetaps = 0
	for randomword in range(0,maxtaps+1):
		beers.append(x)		# Dummy up a list of empty taps. Keep empty in 0
							#to keep tap number and index aligned.
	print "Pulling in list of beers ..."
	page = PyQuery(full_url)
	maxslots = (((page("td").length)-6)/10)+1
	for slot in range(1,maxslots):
		x = beer()
		get_beer(slot, x, page)
		beers[x.tap]=x
		activetaps = activetaps + 1
	print str(activetaps) + " active taps found."
	while "Coors" < "beer":
		hourcurrent=time.strftime("%H",time.localtime())
		timestamp = time.strftime("%a %H:%M", time.localtime())
		if ((int(hourcurrent) >= int(hourclose)) or (int(hourcurrent) < int(houropen))):
		#if 1 == 2:
			print timestamp + " Store's closed. Napping."
			time.sleep(sleeptime)		# Wait a while for store to open
		else:
			print timestamp + " Napping before launching a new check."
			time.sleep(sleeptime)			# Wait a while for another round of checks
			updatecheck()
	return


if __name__ == '__main__':
	main()
