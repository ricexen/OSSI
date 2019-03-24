import os
from src.util import write_directory, join_path
from src.terminal import Terminal

user_request_exit = False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = join_path(ROOT_DIR, 'output')
OUTPUT_REQUESTS_DIR = join_path(ROOT_DIR, 'output/requests')
OUTPUT_CSVS_DIR = join_path(ROOT_DIR, 'output/csv')
OUTPUT_FRIENDS = join_path(OUTPUT_CSVS_DIR, 'friends')
COOKIES_DIR = join_path(ROOT_DIR, 'cookie')
CONFIGURATION_DIR = join_path(ROOT_DIR, 'configuration')


def define_directories():
  # directories
  DIRS = [
    OUTPUT_DIR, 
    COOKIES_DIR, 
    CONFIGURATION_DIR, 
    OUTPUT_REQUESTS_DIR, 
    OUTPUT_CSVS_DIR
  ]
  for dir_path in DIRS:
    write_directory(dir_path)

terminal = Terminal()
terminal.logo('Open Source Information Facebook')