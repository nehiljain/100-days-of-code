import base64

import twitter
import logging
import json
from github import Github
from cucco import Cucco

from config import config

log_url = 'https://goo.gl/rkDuXu'
consumer_key         = config['TWITTER']['CONSUMER_KEY']
consumer_secret      = config['TWITTER']['CONSUMER_SECRET']
access_token_key     = config['TWITTER']['ACCESS_TOKEN_KEY']
access_token_secret  = config["TWITTER"]['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

git = Github(config['GITHUB']['USER'], config['GITHUB']['PASSWORD'])


def clean_str_for_update(s):
  '''
    Make all characters in lower case.
    Replace all spaces, special characters with '_'
    Drop all the trailing characters '-' and '_'
    Add character 'x' if the string starts with number(s)
  '''
  try:
    assert (isinstance(s, str) and len(s) > 0), 'The column name is invalid'
    cucco = Cucco()
    normalizations = [
      'remove_extra_white_spaces',
      'remove_accent_marks',
      ('replace_characters', {'characters': ['-', '*'], 'replacement': '' })
    ]
    new_s = cucco.normalize(s, normalizations).strip('-_\n ')
    return new_s
  except Exception as e:
    logging.exception('Error while cleaning column name')
    raise


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
  for update in updates[-1:]:
    if 'links to work' in update.lower():
      update_text, link = update.split('**Links to work:**')
      update_texts = update_text.split('\n')
      update_texts_notnull = [clean_str_for_update(s) for s in update_texts if s]
      day_str = update_texts_notnull[0].split(':')[0]
      update_texts_notnull = [s for s in update_texts_notnull[1:] if "Today's Progress" not in s]
      progress_text = update_texts_notnull[0]
      return day_str, progress_text


def generate_tweet_from_update(day_str, update):
  update = '''{}: {} #100DaysOfCode ProgressLogs @ {} 
  '''.format(day_str, update, log_url)
  return update


if __name__ == '__main__':
  day_str, text = get_progress_from_github()
  api.PostUpdate(generate_tweet_from_update(day_str, text))


