import argparse
import json
from nicovideo_api import NicovideoAPI
from sound_extractor import SoundExtractorFactory
from config import Config

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='gazeru is niconico downloader')
    argparser.add_argument('-l', '--list',help='display registered mylist', action='store_true')
    argparser.add_argument('-a', '--add', help='add mylist')
    argparser.add_argument('-u', '--user', nargs=2, help='set user and password')
    argparser.add_argument('-d', '--directory', help='set download directory')
    args = argparser.parse_args()

    if args.list:
        config = Config()
        print('{0:10} {1:10} {2}'.format('id', 'creator', 'title'))
        for mylist in config.get_mylists():
            print('{0:10} {1:10} {2}'.format(mylist['id'], mylist['creator'], mylist['title']))

    if args.add:
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
    if args.user:
        user = args.user[0]
        password = args.user[1]
        config = Config()
        config.set_user(user)
        config.set_password(password)

    if args.directory:
        """引数で渡されたディレクトリ を config ファイルに書き込んで、
        該当のディレクトリに.gazeruファイルを設置する
        .gazeruファイルは mylist_id: [{ダウンロードされたvideo_id: ファイル名}] という形式で書き込まれる
        """
        directory = args.directory
        dot_gazeru = '{0}/.gazeru'.format(directory)
        with open(dot_gazeru, 'w') as file:
            config = Config()
            mylists = config.get_mylists()
            file.write(json.dumps({mylist['id']:[] for mylist in mylists}))
        config = Config()
        config.set_directory(directory)
