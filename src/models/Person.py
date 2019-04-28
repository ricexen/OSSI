from src.api import Facebook
from src.util import save_list_of_dicts
from definitions import OUTPUT_CSVS_DIR

people_file = '%s/people.csv' % OUTPUT_CSVS_DIR
people_connections_file = '%s/people_connections.csv' % OUTPUT_CSVS_DIR

fb_api = Facebook()


class Person:
    def __init__(self, id=None, name=None, load_information=True, load_photo=True):
        self.profile = {}
        self.name = {'full': name}
        self.id = id
        if self.id and load_information:
            self.profile = fb_api.get_profile_data(self.id)
            self.id = self.profile.get('id', None)
            self.email = self.profile.get('email', None)
            self.gender = self.profile.get('gender', None)
            self.birthday = self.profile.get('birthday', None)
            self.name = {
                'first': self.profile.get('first_name', ''),
                'last': self.profile.get('last_name', ''),
                'user': self.profile.get('username', None)
            }
            fullname = '%s %s' % (self.name['first'], self.name['last'])
            self.name['full'] = fullname.strip()
            self.knowns = []
            self.connections = []
            self.photo = None
        if self.id and load_photo:
            self.load_photo()
        self.save()

    def load_knowns(self, depth=0, reverse=False, origin=None):
        if not origin:
            origin = self.id
        if self.id:
            for known_raw in fb_api.get_knowns_of(self.id):
                id = known_raw.get('id', None)
                name = known_raw.get('name', None)
                known = Person(id, name, load_information=False,
                               load_photo=False)
                connection = {
                    'source': self.id,
                    'target': known.id
                }
                self.connections.append(connection)
                self.knowns.append(known)
        if depth > 0:
            for index, known in enumerate(self.knowns):
                id = known.id
                k = self.knowns[index] = Person(id=id, load_photo=False)
                k.load_knowns(depth=depth - 1)

    def has_knowns(self):
        return self.knowns and len(self.knowns)

    def load_photo(self):
        self.photo = fb_api.get_profile_picture(self.id).name

    def save(self):
        d = self.__dict__
        data = {
            'name': d['name']['full'],
            'id': d['id'],
            'birthday': d.get('birthday', None),
            'email': d.get('email', None),
            'gender': d.get('gender', None),
            'photo': d.get('photo', None),
        }
        fields = list(data)
        save_list_of_dicts(people_file, [data], fields)

    def save_connections(self):
        fields = ['source', 'target']
        save_list_of_dicts(people_connections_file, self.connections, fields)
