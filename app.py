#!/usr/bin/env python
import shelve
from subprocess import check_output
import flask
from flask import request, Flask, render_template, jsonify, abort, redirect
from os import environ

import os
import sys
import json
import hashlib

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
	print "sdhfjhfsdhfa"
	long_URL = str(request.form['longURL'])
	#print "long url is ",long_URL
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
