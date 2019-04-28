import os
import csv
from facebook import GraphAPIError
from src.terminal import Terminal
from src.util import write_directory, save_list_of_dicts
from definitions import OUTPUT_CSVS_FRIENDS_DIR, OUTPUT_CSVS_DIR
from src.actions import facebook_api
from progress.bar import Bar as ProgressBar
from progress.spinner import Spinner


class Person:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.photo = kwargs.get('photo', None)
        self.knowns = []
        self.connections = []

    def get_knowns(self, depth=0, reverse=False):
        knowns = []
        if self.id:
            knowns = facebook_api.get_knowns_of(self.id)
        for known in knowns:
            person = Person(id=known['id'], name=known['name'])
            self.connections.append({
                'source': self.id,
                'target': known['id']
            })
            self.knowns.append(person)
        if (depth > 0):
            for known in self.knowns:
                known.get_knowns(depth - 1, reverse)
        return self.knowns

    def has_knowns(self):
        return len(self.knowns) > 0


def find_knowns_of(terminal: Terminal, params: dict):
    profile_id = params.get('id', None)
    if not profile_id:
        terminal.error('No profile id provided')
        terminal.info('Try again using -profile-id=<profile id>')
        return
    else:
        terminal.info('Getting knowns of %s' % profile_id)
        try:
            knowns_of = facebook_api.get_knowns_of(profile_id)
            if len(knowns_of) > 0:
                known_directory = '%s/%s' % (
                    OUTPUT_CSVS_FRIENDS_DIR, profile_id)
                file_name = '%s/known_people.csv' % known_directory
                try:
                    os.mkdir(known_directory)
                except FileExistsError:
                    pass
                save_list_of_dicts(file_name, knowns_of, ['id', 'name'])
        except GraphAPIError as ex:
            terminal.error(str(ex))


def find_knowns_of_my_knowns(terminal: Terminal):
    terminal.info('Getting knowns of all')
    knowns = facebook_api.get_knowns()
    for known in knowns:
        find_knowns_of(terminal, {'id': known['id']})


def uniquify(array: list):
    return [dict(y) for y in set(tuple(x.items()) for x in array)]


def get_people(terminal: Terminal):
    people = []
    known_folders = os.listdir(OUTPUT_CSVS_FRIENDS_DIR)
    try:
        progress_bar = ProgressBar(
            'Loading knowns from .csv files', max=len(known_folders))
        for folder in known_folders:
            knowns_file = '%s/%s/known_people.csv' % (
                OUTPUT_CSVS_FRIENDS_DIR, folder)
            if os.path.exists(knowns_file):
                with open(knowns_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for individual in reader:
                        people.append(individual)
                    f.close()
            progress_bar.next()
        print()
        with open('%s/known_people.csv' % OUTPUT_CSVS_DIR, 'r') as f:
            reader = csv.DictReader(f)
            progress_bar_knowns = ProgressBar(
                'Loading knowns from .csv files', max=sum(1 for row in reader) - 1)
            for individual in reader:
                people.append(individual)
                progress_bar_knowns.next()
            f.close()
    except FileNotFoundError as ex:
        terminal.error(str(ex))
    return uniquify(people)


def get_known_connections(person, connections=[]):
    if person.has_knowns():
        for known in person.knowns:
            for con in known.connections:
                connections.append(con)
            get_known_connections(known, connections)
    return connections


def get_connections(terminal: Terminal):
    people_file = '%s/people.csv' % OUTPUT_CSVS_DIR
    connections_file = '%s/people_connections.csv' % OUTPUT_CSVS_DIR
    connections = []
    people = []
    persons = []
    if not os.path.exists(people_file):
        terminal.info('Generating people file')
        people = get_people(terminal)
        save_list_of_dicts(people_file, people, ['id', 'name'])
    with open(people_file, 'r') as f:
        terminal.info('Reading file: %s' % people_file)
        reader = csv.DictReader(f)
        for row in reader:
            person = Person(id=row['id'], name=row['name'])
            persons.append(person)

    for person in persons:
        person.get_knowns(0)
        for con in get_known_connections(person):
            connections.append(con)
    save_list_of_dicts(connections_file, connections, ['source', 'target'])


def genderify_photos(terminal):
    pass


def find_knowns_of_depth(terminal):
    pass
