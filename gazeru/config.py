import os
import json

class Config():
    def __init__(self):
        HOME = os.environ['HOME']
        self.configfile = '{0}/.gazeru/gazeru.conf'.format(HOME)
        with open(self.configfile, 'r') as configfile:
            config = configfile.read()
        self.config = json.loads(config)

    def get_mylists(self):
        return self.config['mylist']

    def set_user(self, user):
        self.config['account']['user'] = user
        self._save()

    def get_user(self):
        return self.config['account']['user']

    def set_password(self, password):
        self.config['account']['password'] = password
        self._save()

    def get_password(self):
        return self.config['account']['password']

    def add_mylist(self, mylist):
        self.config['mylist'].append(mylist)
        self._save()

    def set_directory(self, directory):
        self.config['directory'] = directory
        self._save()

    def get_directory(self):
        return self.config['directory']

    def _save(self):
         with open(self.configfile, 'w') as configfile:
            configfile.write(json.dumps(self.config))
