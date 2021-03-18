import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from api import API
from db import MySQLDB

# Load .env file with creds
load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

api = API(consumer_key, consumer_secret, access_token, access_token_secret)
db = MySQLDB(host="localhost", user="root", passwd="password", database="twitter-sample")

app = Flask(__name__)

@app.route("/login")
def login():
	try:
		api.login()
		return {"success" : True}
	except Exception as err:
		return False

@app.route("/userDetails")
def user_details():
	if not api.is_logged_in():
		return jsonify({"success" : False, "msg" : "User not logged in."})

	try:
		# Get data from API
		data = api.user_details()
		print (data)
		# Ingest into DB
		db.insert_user(data)
		print ("inserted")
		# Send data from DB
		return jsonify(db.get_user(data.get("user_id")))
	except Exception as err:
		return jsonify({"success" : False, "msg" : str(err)})



@app.route("/userFollowers")
def user_followers():
	if not api.is_logged_in():
		return False

	try:
		# Get data from API
		data = api.user_followers()
		# Ingest into DB
		for follower in data.get('followers'):
			db.insert_follower(follower)
		# Send data from DB
		return jsonify(db.get_user_followers(data.get('followers')[0].get("user_id")))
	except Exception as err:
		return jsonify({"success" : False, "msg" : str(err)})

	return {"success" : True}

@app.route("/userTweets")
def user_tweets():
	if not api.is_logged_in():
		return False

	try:
		# Get data from API
		data = api.user_tweets()
		print (data)
		# Ingest into DB
		for tweet in data.get('tweets'):
			db.insert_tweet(tweet)
		# Send data from DB
		return jsonify(db.get_user_tweets(data.get('tweets')[0].get("user_id")))
	except Exception as err:
		return jsonify({"success" : False, "msg" : str(err)})

	return {"success" : True}

# @app.route("/userTimeline")
# def user_timeline():
# 	if not api.is_logged_in():
# 		return False

# 	try:
# 		# Get data from API
# 		data = api.home_timeline()
# 		# Ingest into DB
# 		for tweet in data.get('timeline'):
# 			db.insert_tweet(follower**)
# 		# Send data from DB
# 		return db.get_user_tweets(data.get("user_id"))
# 	except Exception as err:
# 		return False

# 	return {"success" : True}

@app.route("/tweet")
def tweet():
	if not api.is_logged_in():
		return False

	api.tweet(status=request.data.get("status"))

	return {"success" : True}

if __name__ == '__main__':
	app.run(port=5000)
