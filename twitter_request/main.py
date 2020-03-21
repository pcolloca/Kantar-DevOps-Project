import tweepy
import json

consumer_key = "token"
consumer_secret = "token"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Construct the API instance
api = tweepy.API(auth)

tags = ["openbanking", "apifirst", "devops", "devops", "microservices", "apigateway",
		"oauth", "swagger", "raml", "openapis"]

category = []
for tag in tags:
	c = tweepy.Cursor(api.search, q=f"(#{tag})", result_type="recent")

	tweets = []
	for tweet in c.items(100):
		tweets.append({"text":tweet.text, "date": str(tweet.created_at), "user":tweet.author.screen_name, "location":tweet.author.location,
			"followers": tweet.author.followers_count, "lang":tweet.lang})

	category.append({f"{tag}":tweets})

with open("tweets.json", "w") as f:
	f.write(json.dumps(category))
