import pymysql.cursors
import flask

app = flask.Flask(__name__)

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

	def db_query(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
	def __del__(self):
		self.cursor.close()
		self.conn.close()


def top_followers():
	db = DBManager()
	response = db.db_query("SELECT DISTINCT user, MAX(followers) AS 'followers' FROM tweets GROUP BY user ORDER BY MAX(followers) DESC LIMIT 5")
	del db
	return response

def total_posts():
	db = DBManager()
	response = db.db_query("""SELECT HOUR(`date`) AS 'hour' , DAY(`date`) AS 'day', MONTH(`DATE`) AS 'month', COUNT(*) AS 'posts' FROM tweets GROUP BY HOUR(`date`),
							DAY(`date`),MONTH(`DATE`) ORDER BY DAY(`date`) ASC, HOUR(`date`) ASC, MONTH(`DATE`) ASC""")
	del db
	return response

def posts_language():
	db = DBManager()
	response = db.db_query("SELECT hashtag, language, COUNT(*) AS 'posts' FROM tweets GROUP BY hashtag, language")
	del db
	return response


def send_response(responseObj):
	response = flask.jsonify(responseObj)
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Methods', 'GET')
	response.headers.add('Access-Control-Allow-Headers', 'accept,content-type,Origin,X-Requested-With,Content-Type,access_token,Accept,Authorization,source')
	response.headers.add('Access-Control-Allow-Credentials', True)
	return response


@app.route("/get_info", methods=["GET"])
def json_output():
	requested = flask.request.args.get('id')
	print(requested)
	if requested is None:
		return send_response({"error": {"reason": "invalidParameter", "message": "No parameter was given", "code": 400}})
	elif requested == "1":
		return send_response(top_followers())
	elif requested == "2": 
		return send_response(total_posts())
	elif requested == "3": 
		return send_response(posts_language())
	else:
		return send_response({"error": {"reason": "invalidParameter", "message": "No parameter was given", "code": 400}})

if __name__ == '__main__':
	app.run(host='localhost')