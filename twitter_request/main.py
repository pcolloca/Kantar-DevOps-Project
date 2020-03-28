from tqdm import tqdm

import pymysql.cursors
import tweepy

consumer_key = "token"
consumer_secret = "token"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Construct the API instance
api = tweepy.API(auth)

# Hashtags to be stored
tags = ["openbanking", "apifirst", "devops", "devops", "microservices", "apigateway",
		"oauth", "swagger", "raml", "openapis"]

class DBManager():
	def __init__ (self):
		self.conn = pymysql.connect(host='database',
							 port=3306,
							 user='root',
							 password='secret',
							 db='twitter',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor,
							 connect_timeout=60)
		self.cursor = self.conn.cursor()

	def db_commit(self, query):
		self.cursor.execute(query)
		self.conn.commit()

	def db_query(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
	def __del__(self):
		self.cursor.close()
		self.conn.close()


def main():
	db = DBManager()
	lenght = db.db_query("SELECT COUNT(*) AS 'total' FROM tweets")
	lenght = lenght[0]['total']

	for tag in tqdm(tags, position=0):
		c = tweepy.Cursor(api.search, q=f"(#{tag})", result_type="recent")

		for tweet in tqdm(c.items(100), position=1, total=100, leave=False, miniters=1, desc=f"searching {tag}"):
			text = tweet.text
			text = text.replace("'", '"')
			date = str(tweet.created_at)
			user = tweet.author.screen_name
			location = tweet.author.location
			followers = tweet.author.followers_count
			lang = tweet.lang

			query = f"INSERT INTO tweets (hashtag, `text`, `date`, user, location, followers, language) VALUES (\'{tag}\', \'{text}\', \'{date}\', \'{user}\', \'{location}\', {followers}, \'{lang}\');"
			try:
				db.db_commit(query)
			except Exception as e:
				print(e)

	if lenght > 0:
		db.db_commit(f"DELETE FROM tweets LIMIT {lenght}")
	
	del db

if __name__ == '__main__':
	main()