import schedule
import time
import os
import tweepy
from slack_sdk import WebClient
from dotenv import load_dotenv
# 1. Initialization and Authentication
# Load environment variables from .env file
load_dotenv()

# Authenticate with Twitter API
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Authenticate with Slack API
slack_token = os.environ.get("SLACK_TOKEN")
client = WebClient(token=slack_token)

# Initialize count for number of iteration of completed job task
count = 1

