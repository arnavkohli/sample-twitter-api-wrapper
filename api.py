import tweepy

class API:
	def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.auth.set_access_token(access_token, access_token_secret)
		self.api = None

	def is_logged_in(self):
		return True if self.api else False

	def login(self):
		self.api = tweepy.API(self.auth)

	def tweet(self, status):
		if not self.api:
			raise Exception("User not logged in.")
		self.api.update_status(status)

	def user_details(self):
		data = self.api.me()
		return {"user_id" : data.id, "name" : data.name, "screen_name" : data.screen_name}

	def user_followers(self):
		data = self.api.me()
		followers = self.api.followers()
		return {"followers": [{"follower_id" : f.id, "user_id": data.id, "name" : f.name, "screen_name" : f.screen_name} for f in followers], "count" : len(followers)}

	def user_tweets(self):
		data = self.api.me()
		tweets = self.api.user_timeline()
		return {"tweets" : [{"tweet_id" : tweet.id, "user_id": data.id, "text" : tweet.text} for tweet in tweets]}