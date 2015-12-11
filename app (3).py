#!/usr/bin/env python
import shelve
from subprocess import check_output
import flask
from flask import request, Flask, render_template, jsonify, abort, redirect
from os import environ

import urllib2
import json
import oauth2
from operator import itemgetter, attrgetter, methodcaller

import os
import sys
import json
import hashlib

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from googlemaps.client import Client

app = flask.Flask(__name__)
app.debug = True

# Database/Dictionary to save shortened URLs
db = shelve.open("shorten.db")








@app.route('/')
def index():
    """
    Builds a template based on a GET request, with some default
    arguments
    """

    return flask.render_template('index.html')

# if request.method == 'POST':
	# long_URL = request.form.get("longURL")
	# short_URL = request.form.get("shortURL")
	# shorten[short_URL] = long_URL
	#Do stuff
	#render_template("wiki_post.html", longURL=long_URL, shortURL=short_URL)
    #return jsonify(result='Entry has been added')

@app.route("/results", methods=['POST'])
def results():
    # """
    # This POST request creates an association between a short url and a full url
    # and saves it in the database (the dictionary db)
    # """
    #raise NotImplementedError 
	# long_URL = request.form.get("longURL")
	# short_URL = request.form.get("shortURL")
	
	def user_address_details(user_address):
		client = Client(key = "AIzaSyCukzR1OSSqPFI9uI50_XzAZs7F_EQUT1M")
		listy = []
		# exactaddress ="1 Toronto Street Toronto"
		# cor = client.geocode(exactaddress)
		cor = client.geocode(user_address)
		# listy= cor[0]['geometry']['location'][0],cor[0]['geometry']['location'][1]
		# print listy
		return cor[0]['geometry']['location']['lat'],cor[0]['geometry']['location']['lng']


	session = Session(server_token='Y2S9n1LkZaa0ZfN6HIZsG5prWOAfWKRJx7Q7kHEh')
	client = UberRidesClient(session)
	#response = client.get_products(37.77, -122.41)
	def uber_details(src_lat, src_long, dest_lat, dest_long):
		response_1 = client.get_price_estimates(src_lat, src_long,dest_lat, dest_long)
		estimates = response_1.json.get('prices')
		return estimates[0]["estimate"],estimates[0]["duration"]/60, estimates[0]["distance"]
	
	
	
	
	CONSUMER_KEY = 'fOakpV5xYztpUWSwmNJ1bA'
	CONSUMER_SECRET = 'DddxIR2AAUo5ivt5j4JSUXdTZlg'
	TOKEN = 'jhrCPbC7obw49yYQAvTJu9MYbsQJ5Xxv'
	TOKEN_SECRET = '8uPlD4GHliD2G338f57z08bf44M'

	# yelp_req() function description:
	# The input is a url link, which you use to make request to Yelp API, and the 
	# return of this function is a JSON object or error messages, including the information 
	# returned from Yelp API.
	# For example, when url is 'http://api.yelp.com/v2/search?term=food&location=San+Francisco'
	# yelp_req(url) will return a JSON object from the Search API

	def yelp_req(url):
		""" Pass in a url that follows the format of Yelp API,
			and this function will return either a JSON object or error messages.
		"""
		#print "#########################"+url
		oauth_request = oauth2.Request('GET', url, {})
		oauth_request.update(
			{
				'oauth_nonce': oauth2.generate_nonce(),
				'oauth_timestamp': oauth2.generate_timestamp(),
				'oauth_token': TOKEN,
				'oauth_consumer_key': CONSUMER_KEY
			}
		)
		consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
		token = oauth2.Token(TOKEN, TOKEN_SECRET)
		oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
		signed_url = oauth_request.to_url()

		conn = urllib2.urlopen(signed_url, None)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()
		#jsonfile.write(response)
		return response

	#################################################################################
	# Your code goes here
	restfile = open('restaurants2.txt', 'w')
	#jsonfile = open('restaurants.json', 'w')
	city = request.form.get("city")
	#city=city.encode('ascii')
	urlRB='http://api.yelp.com/v2/search?term=restaurants&location=%s&limit=20&sort=2' % city
	print "Here is ****************************",urlRB
	JResponse = yelp_req(urlRB)
	#restfile.write(JResponse)
	#print JResponse[u'businesses'][0][u'name'], "####",int(JResponse[u'businesses'][0][u'review_count'])
	#arrayRest= {"Restaurant name", review_count, Restaurant_address, 
	#rest_latitude, rest_longitude, User_address, user_addrs_latitude, user_addr_longitude, price_estimate, duration, distance}
	arrayRest = [["",0,"",0,0,"User Address",0,0,0,0,0] for i in range(20)]
	#bNames=JResponse[2]
	#print bNames
	user_address=request.form.get("useraddress")
	for i in range(20):
		#arrayRest[i]=[JResponse[u'businesses'][i][u'name'].encode("utf-8"),JResponse[u'businesses'][i][u'review_count'],JResponse[u'businesses'][i][u'location'][u'address'].encode("utf-8"),JResponse[u'businesses'][i][u'location'][u'coordinate'][u'latitude'],JResponse[u'businesses'][i][u'location'][u'coordinate'][u'longitude'],0,0,0,0,0]
		arrayRest[i]=[JResponse[u'businesses'][i][u'name'],JResponse[u'businesses'][i][u'review_count'],JResponse[u'businesses'][i][u'location'][u'address'][0],JResponse[u'businesses'][i][u'location'][u'coordinate'][u'latitude'],JResponse[u'businesses'][i][u'location'][u'coordinate'][u'longitude'],"User address",0,0,0,0,0]
		arrayRest[i][5]=user_address
		arrayRest[i][6],arrayRest[i][7]=user_address_details(user_address)
		arrayRest[i][8],arrayRest[i][9],arrayRest[i][10]=uber_details(arrayRest[i][6],arrayRest[i][7],JResponse[u'businesses'][i][u'location'][u'coordinate'][u'latitude'],JResponse[u'businesses'][i][u'location'][u'coordinate'][u'longitude'])	
	
	arrayRestSorted=sorted(arrayRest, key=itemgetter(1))
	
	
	return render_template("results.html", arrayRestSorted=arrayRestSorted)
	
	
	# print "sdhfjhfsdhfa"
	# long_URL = str(request.form['longURL'])
	# short_URL = str(request.form['shortURL'])
	# db.update({short_URL: long_URL});
	
	#return render_template("restaurants.bahirwani.txt")#, longURL=long_URL, shortURL=short_URL)


	
	
	
	

@app.route('/URL')
def index2():
    """
    Builds a template based on a GET request, with some default
    arguments
    """

    return flask.render_template('index2.html')

###
# Now we'd like to do this generally:
# <short> will match any word and put it into the variable =short= Your task is
# to store the POST information in =db=, and then later redirect a GET request
# for that same word to the URL provided.  If there is no association between a
# =short= word and a URL, then return a 404
###

# if request.method == 'POST':
	# long_URL = request.form.get("longURL")
	# short_URL = request.form.get("shortURL")
	# shorten[short_URL] = long_URL
	#Do stuff
	#render_template("wiki_post.html", longURL=long_URL, shortURL=short_URL)
    #return jsonify(result='Entry has been added')

@app.route("/create", methods=['POST'])
def create():
    # """
    # This POST request creates an association between a short url and a full url
    # and saves it in the database (the dictionary db)
    # """
    #raise NotImplementedError 
	# long_URL = request.form.get("longURL")
	# short_URL = request.form.get("shortURL")
	long_URL = str(request.form['longURL'])
	short_URL = str(request.form['shortURL'])
	db.update({short_URL: long_URL});
	
	return render_template("wiki_post.html", longURL=long_URL, shortURL=short_URL)	
	
	
	
	
	
	
	
@app.route("/short/<short>", methods=['GET'])
def load_redirect(short):
	# Redirect the request to the URL associated =short=, otherwise return 404# NOT FOUND
	#print db.has_key(str(short))
	#print db[str(short)]
	try :
		if db[str(short)]:
			return redirect("http://"+db[str(short)], code=301)
		else:
			return "HTTP_404_NOT_FOUND"
	except Exception:
		return "HTTP_404_NOT_FOUND"
	# if db.has_key(str(short)):
		# return redirect(db[str(short)])
	# else:
		# return "HTTP_404_NOT_FOUND"
		
		
	# else: # If the method is either POST or PUT
		# # Change the redirect path to the parameter named "name"
		# redirect_db["location"] = request.form.get('location', "http://ischool.berkeley.edu").strip() # Remove newline at end of telnet requests
		# #redirect_db["location"] = str(request.form.get("location")).strip() # Remove newline at end of telnet requests
		# return render_template("redirect.html", location=redirect_db["location"])
		# #return redirect(redirect_db["location"], code=200)
    # raise NotImplementedError 
	

if __name__ == "__main__":
    app.run()
