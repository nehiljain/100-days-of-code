import base64

import twitter
import logging
import json
from github import Github
from config import config
consumer_key         = config['TWITTER']['CONSUMER_KEY']
consumer_secret      = config['TWITTER']['CONSUMER_SECRET']
access_token_key     = config['TWITTER']['ACCESS_TOKEN_KEY']
access_token_secret  = config["TWIITER"]['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

git = Github(config['GITHUB']['USER'], config['GITHUB']['PASSWORD'])


def check_credcentials(api):
  try:
    api.VerifyCredentials()
  except Exception as e:
    logging.exception('Credentials do not work')
    raise

def post_update(msg):
  try:
    status = api.PostUpdate(msg)
    return 'Posted' + json.dumps(status)
  except Exception as e:
    logging.exception('Failed to post')
    raise

def get_progress_from_github():
  repo = git.get_user().get_repo('100-days-of-code')
  progress_logs_file = repo.get_file_contents('log.md')
  progress_logs = str(base64.standard_b64decode(progress_logs_file.content).decode('utf-8'))
  updates = progress_logs.split("###")
  for update in updates:
    if 'kinks to work' in update.lower():
      update_text, link = update.split('**Links to work:**')




def get_update_for_date(update_date):
  pass

def generate_tweet_from_update(update_date, update_log):
  pass




get_progress_from_github()


