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


# 2. Job Task
# Retrieve 10 latest tweets from Twitter and display at Slack channel #general
def job():
    global count
    client.chat_postMessage(channel='#general', text="########")
    client.chat_postMessage(channel='#general', text="Hourly Update from Twitter")
    jobAnnounce()
    client.chat_postMessage(channel='#general', text="########")
    print("Code Starting")
    # Get tweets from specified Twitter account
    try:
        tweets = tweepy.Cursor(api.user_timeline, screen_name='livelyrahul', count=10).items()
    except tweepy.error.RateLimitError as e:
        print(e)
    finally:
        print("Code Run " + str(count-1) + " Completed")

    # Post tweets to designated Slack channel
    for tweet in tweets:
        try:
            client.chat_postMessage(channel='#general', text=tweet.text)
        except Exception as e:
            print(e)
    client.chat_postMessage(channel='#general', text="### Hourly Update from Twitter over ###")
    return


# Measure count of tweet retrieved and pass as comment in the slack bot
def jobAnnounce():
    global count
    client.chat_postMessage(channel='#general', text=str(count))
    count += 1
    return

# 3. Schedule handling
# Schedule the job to run 1 hour
try:
    schedule.every(1).hour.do(job)
except Exception as e:
    print(e)
finally:
    print("Code Running Count : "+str(count))

# While loop to run app continuously
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as e:
    print(e)
finally:
    print("Code Exiting")
