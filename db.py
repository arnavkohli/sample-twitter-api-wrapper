import mysql.connector

def double_stringify(val):
	return '"' + val + '"'

def stringify(val):
	return "'" + val + "'"

def prettify(data, columns):
	return {col: d for col, d in zip(columns, data)}

class MySQLDB:

	def __init__(self, host, user, passwd, database):
		self.db = mysql.connector.connect(
			host=host, 
			user=user, 
			passwd=passwd, 
			database=database)
		self.cursor = self.db.cursor()
		print ('[+] Connection to DB successful')


	def get_user(self, user_id):
		columns = ("user_id", "name", "screen_name")
		query = f"select * from user where user_id = {user_id}"
		self.cursor.execute(query)
		return prettify(self.cursor.fetchone(), columns)

	def get_user_tweets(self, user_id):
		columns = ("tweet_id", "user_id", "text")
		query = f"select * from user_tweets where user_id = '{user_id}'"
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		return [prettify(res, columns) for res in result]

	def get_user_followers(self, user_id):
		columns = ("follower_id", "user_id", "name", "screen_name")
		query = f"select * from user_followers where user_id = '{user_id}'"
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		return [prettify(res, columns) for res in result]

	def insert_user(self, data):
		first = "insert into {} (".format("user")
		second = "values ("

		for key, val in data.items():
			first += key.lower() + ", "
			if key == 'user_id':
				second += str(val) + ", "
			else:
				second += stringify(val) + ", "

		query = first[:-2] + ")" + " " + second[:-2] + ")"
		try:
			self.cursor.execute(query)
		except mysql.connector.errors.IntegrityError:
			return False, 'duplicate entry'
			pass
		self.db.commit()
		return True, 'success'

	def insert_tweet(self, data):
		first = "insert into {} (".format("user_tweets")
		second = "values ("

		for key, val in data.items():
			first += key.lower() + ", "
			if key == 'user_id' or key == 'tweet_id':
				second += str(val) + ", "
			else:
				second += double_stringify(val) + ", "

		query = first[:-2] + ")" + " " + second[:-2] + ")"
		try:
			self.cursor.execute(query)
		except mysql.connector.errors.IntegrityError:
			return False, 'duplicate entry'
			pass
		self.db.commit()
		return True, 'success'

	def insert_follower(self, data):
		first = "insert into {} (".format("user_followers")
		second = "values ("

		for key, val in data.items():
			first += key.lower() + ", "
			if key == 'user_id' or key == 'follower_id':
				second += str(val) + ", "
			else:
				second += stringify(val) + ", "

		query = first[:-2] + ")" + " " + second[:-2] + ")"
		try:
			self.cursor.execute(query)
		except mysql.connector.errors.IntegrityError:
			return False, 'duplicate entry'
			pass
		self.db.commit()
		return True, 'success'
