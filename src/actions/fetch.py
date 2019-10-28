import csv
from progress.bar import Bar as ProgressBar
from definitions import OUTPUT_CSVS_DIR
from src.actions import facebook_api
from src.util import save_list_of_dicts


def token_not_generated(terminal, ex):
    terminal.error(str(ex))
    terminal.warning('Token has not been generated')
    terminal.info('Eject "token" command to get it.')


def fetch_knowns(terminal):
    terminal.write('-' * 44)
    knowns = []
    try:
        knowns = facebook_api.get_knowns()
    except IOError as ex:
        token_not_generated(terminal, ex)
    save_list_of_dicts('%s/known_people.csv' %
                       OUTPUT_CSVS_DIR, knowns, ['id', 'name'])
    terminal.info('%s knowns found' % len(knowns))


def fetch_photos(terminal):
    terminal.write('-' * 44)
    knowns = []
    try:
        knowns = facebook_api.get_knowns()
    except IOError as ex:
        token_not_generated(terminal, ex)
    progress_bar = ProgressBar('Saving knowns photos', max=len(knowns))
    for known in knowns:
        picture = facebook_api.get_profile_picture(known['id'])
        known['picture'] = picture
        progress_bar.next()
    save_list_of_dicts('%s/known_people.csv' %
                       OUTPUT_CSVS_DIR, knowns, ['id', 'name', 'picture'])
    terminal.info('%s knowns found' % len(knowns))


def fetch_ids(terminal):
    terminal.write('-' * 44)
    try:
        knowns = facebook_api.get_knowns()
    except IOError as ex:
        token_not_generated(terminal, ex)
    save_list_of_dicts('%s/known_ids.csv' % OUTPUT_CSVS_DIR, knowns, ['id'])
    terminal.info('%s knowns found' % len(knowns))


def fetch_phones(terminal):
    terminal.write('-' * 44)
    phones = []
    try:
        knowns = facebook_api.get_knowns()
    except IOError as ex:
        token_not_generated(terminal, ex)
    progress_bar = ProgressBar('Fetching phones', max=len(knowns))
    for known in knowns:
        known_data = facebook_api.get_profile_data(known['id'])
        known['phone'] = known_data.get('mobile_phone', None)
        phones.append(known['phone'])
        progress_bar.next()
    save_list_of_dicts('%s/known_phones.csv' %
                       OUTPUT_CSVS_DIR, knowns, ['id', 'name', 'phone'])
    terminal.info('%s/%s phones found' % (len(knowns), len(phones)))


def fetch_emails(terminal):
    terminal.write('-' * 44)
    emails = []
    try:
        knowns = facebook_api.get_knowns()
    except IOError as ex:
        token_not_generated(terminal, ex)
    progress_bar = ProgressBar('Fetching emails', max=len(knowns))
    for known in knowns:
        known_data = facebook_api.get_profile_data(known['id'])
        known['email'] = known_data.get('email', None)
        emails.append(known['email'])
        progress_bar.next()
    save_list_of_dicts('%s/known_emails.csv' %
                       OUTPUT_CSVS_DIR, knowns, ['id', 'name', 'email'])
    terminal.info('%s/%s emails found' % (len(knowns), len(emails)))


def fetch_all(terminal):
    terminal.write('-' * 44)
    try:
        knowns = facebook_api.get_knowns()
    except IOError as ex:
        token_not_generated(terminal, ex)
    progress_bar = ProgressBar('Fetching basic data', max=len(knowns))
    for known in knowns:
        known_data = facebook_api.get_profile_data(known['id'])
        picture = facebook_api.get_profile_picture(known['id'])
        known['picture'] = picture.name
        known['phone'] = known_data.get('mobile_phone', None)
        known['email'] = known_data.get('email', None)
        known['username'] = known_data.get('username', None)
        progress_bar.next()
    file_name = '%s/known_all.csv' % OUTPUT_CSVS_DIR
    fields = ['id', 'username', 'name', 'email', 'phone', 'picture']
    save_list_of_dicts(file_name, knowns, fields)
    terminal.info('%s knowns found' % len(knowns))
