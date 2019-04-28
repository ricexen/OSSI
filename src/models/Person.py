from src.api import Facebook

fb_api = Facebook()


class Person:
    def __init__(self, id):
        self.profile = fb_api.get_profile_data(id)
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
        self.photo = None
        self.load_photo()

    def load_photo(self):
        self.photo = fb_api.get_profile_picture(self.id).name
