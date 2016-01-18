import argparse

from nicovideo_api import NicovideoAPI
from sound_extractor import SoundExtractorFactory
from config import Config

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='gazeru is niconico downloader')
    argparser.add_argument('-l', '--list',help='display registered mylist', action='store_true')
    argparser.add_argument('-a', '--add', help='add mylist')
    argparser.add_argument('-u', '--user', nargs=2, help='set user and password')
    args = argparser.parse_args()

    if args.list:
        config = Config()
        print('{0:10} {1:10} {2}'.format('id', 'creator', 'title'))
        for mylist in config.get_mylists():
            print('{0:10} {1:10} {2}'.format(mylist['id'], mylist['creator'], mylist['title']))
    elif args.add:
        mylist_id = args.add
        config = Config()
        mylists = config.get_mylists()
        if args.add in [mylist['id'] for mylist in mylists]:
            print('{0} is already registed'.format(mylist_id))
        else:
            config = Config()
            niconico = NicovideoAPI(config.get_user(), config.get_password())
            mylist_info = niconico.get_mylist_info(mylist_id)
            config.add_mylist({'id': mylist_info['id'], 'creator': mylist_info['creator'], 'title': mylist_info['title']})
    elif args.user:
        user = args.user[0]
        password = args.user[1]
        config = Config()
        config.set_user(user)
        config.set_password(password)
    else:
        config = Config()
