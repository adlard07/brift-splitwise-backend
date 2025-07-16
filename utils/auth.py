from utils.logger import logging
from splitwise import Splitwise
from dotenv import load_dotenv
import json
import os

load_dotenv()

consumer_key = os.getenv('CUSTOMER_KEY')
consumer_secret = os.getenv('CUSTOMER_SECRET')
api_key = os.getenv('API_KEY')

print(f"Customer key:{consumer_key}\nCustomer secret: {consumer_secret}\nAPI key: {api_key}")

s_obj = Splitwise(
		consumer_key=consumer_key,
		consumer_secret=consumer_secret,
		# api_key=api_key,
	)

session = {}
url, secret = s_obj.getAuthorizeURL()
session['secret'] = secret
logging.info(f"Auth url: {url}")
logging.info(f"Auth secret: {secret}")


with open('creds.json', 'r') as f:
	creds = dict(json.load(f))

oauth_token = creds['oauth_token']
oauth_verifier = creds['oauth_verifier']

access_token = s_obj.getAccessToken(
	oauth_token, 
	session['secret'],
	oauth_verifier
	)
