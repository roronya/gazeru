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

    def get_user(self):
        return self.config['account']['user']

    def get_password(self):
        return self.config['account']['password']

    def add_mylist(self, mylist):
        self.config['mylist'].append(mylist)
        with open(self.configfile, 'w') as configfile:
            configfile.write(json.dumps(self.config))
