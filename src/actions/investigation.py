import os, csv
from facebook import GraphAPIError
from src.terminal import Terminal
from src.util import write_directory, save_list_of_dicts
from definitions import OUTPUT_CSVS_FRIENDS_DIR, OUTPUT_CSVS_DIR
from src.actions import facebook_api
from progress.bar import Bar as ProgressBar
from progress.spinner import Spinner

def find_friends_of(terminal: Terminal, params: dict):
  profile_id = params.get('id', None)
  if not profile_id:
    terminal.error('No profile id provided')
    terminal.info('Try again using -profile-id=<profile id>')
    return
  else:
    terminal.info('Getting friends of %s' % profile_id)
    try:
      friends_of = facebook_api.get_friends_of(profile_id)
      if len(friends_of) > 0:
        friend_directory = '%s/%s' % (OUTPUT_CSVS_FRIENDS_DIR, profile_id)
        file_name = '%s/friends.csv' % friend_directory
        try:
          os.mkdir(friend_directory)
        except FileExistsError:
          pass
        save_list_of_dicts(file_name, friends_of, ['id', 'name'])
    except GraphAPIError as ex:
      terminal.error(str(ex))

def find_friends_of_my_friends(terminal: Terminal):
  terminal.info('Getting friends of all')
  friends = facebook_api.get_friends()
  for friend in friends:
    find_friends_of(terminal, {'id': friend['id']})

def uniquify(array: list):
  return [dict(y) for y in set(tuple(x.items()) for x in array)]

def get_people(terminal: Terminal):
  people = []
  friend_folders = os.listdir(OUTPUT_CSVS_FRIENDS_DIR)
  try:
    progress_bar = ProgressBar('Loading friends from .csv files', max=len(friend_folders))
    for folder in friend_folders:
      friends_file = '%s/%s/friends.csv' % (OUTPUT_CSVS_FRIENDS_DIR, folder)
      if os.path.exists(friends_file):
        with open(friends_file, 'r') as f:
          reader = csv.DictReader(f)
          for individual in reader:
            people.append(individual)
          f.close()
      progress_bar.next()
    print()
    with open('%s/friends.csv' % OUTPUT_CSVS_DIR, 'r') as f:
      reader = csv.DictReader(f)
      progress_bar_friends = ProgressBar('Loading friends from .csv files', max=sum(1 for row in reader) - 1)
      for individual in reader:
        people.append(individual)
        progress_bar_friends.next()
      f.close()
  except FileNotFoundError as ex:
    terminal.error(str(ex))
  return uniquify(people)

def friend_connections(terminal:Terminal, friend):
  connections = []
  friend_friends_csv = None
  try:
    friend_friends_csv = open('%s/%s/friends.csv' % (OUTPUT_CSVS_FRIENDS_DIR, friend['id']), 'r')
    friend_friends_csv = csv.DictReader(friend_friends_csv, fieldnames=['id', 'name'])
    next(friend_friends_csv)
  except FileNotFoundError:
    pass
  if friend_friends_csv:
    try:
      with open('%s/people.csv' % OUTPUT_CSVS_DIR, 'r') as f:
        people_reader = csv.DictReader(f, fieldnames=['id'])
        next(people_reader)
        for individual in people_reader:
          for friend_of_friend in friend_friends_csv:
            if individual['id'] == friend_of_friend['id']:
              connection = {
                'source': individual['id'],
                'target': friend['id']
              }
              connections.append(connection)
        f.close()      
    except FileExistsError:
      pass
  return connections

def get_connections(terminal: Terminal):
  people_file = '%s/people.csv' % OUTPUT_CSVS_DIR
  people = []
  if not os.path.exists(people_file):
    people = get_people(terminal)
  if len(people) > 0:
    save_list_of_dicts(people_file, people, ['id', 'name'])
  user_fields = ['id', 'name']
  f = open('%s/friends.csv' % OUTPUT_CSVS_DIR, 'r')
  friends = csv.DictReader(f, fieldnames=user_fields)
  next(friends)
  with open('%s/connections.csv' % OUTPUT_CSVS_DIR, 'w') as connections_csv:
    connections_writter = csv.DictWriter(connections_csv, fieldnames=['source', 'target'])
    connections_writter.writeheader()
    friends = list(enumerate(friends))
    terminal.info('Connecting friends of friends')
    progress_bar = ProgressBar('', max = (len(friends)))
    for friend in friends:
      for connection in friend_connections(terminal, dict(friend[1])):
        connections_writter.writerow(connection)
      progress_bar.next()
  f.close()
  print()


  
  
  

def genderify_photos(terminal):
  pass

def find_friends_of_depth(terminal):
  pass