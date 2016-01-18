import os
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

    elif args.directory:
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

    else:
        config = Config()
        niconico = NicovideoAPI(config.get_user(), config.get_password())
        sound_extractor_factory = SoundExtractorFactory()
        # mylist とそれに登録されている video_id を取得する
        mylists = config.get_mylists()
        all_mylist_info = {mylist['id']: niconico.get_mylist_info(mylist['id']) for mylist in mylists}
        all = {mylist_info['id']: mylist_info['video_list'] for mylist_id,mylist_info in all_mylist_info.items()}
        dot_gazeru = '{0}/.gazeru'.format(config.get_directory())
        with open(dot_gazeru, 'r') as file:
            done = json.loads(file.read())
        not_yet = {mylist_id: [video_id for video_id in video_id_list if video_id not in done[mylist_id]] for mylist_id,video_id_list in all.items()}
        for mylist_id,video_id_list in not_yet.items():
            for video_id in video_id_list:
                video_info = niconico.get_thumb_info(video_id)
                video = niconico.get_flv(video_id)
                sound_extractor = sound_extractor_factory.build(video, video_info['movie_type'])
                sound = sound_extractor.extract(video)
                sound_file_path = '{0}/{1}'.format(config.get_directory(), all_mylist_info[mylist_id]['creator'])
                os.makedirs(sound_file_path, exist_ok=True)
                sound_file = '{0}/{1}.{2}'.format(sound_file_path, video_info['title'], sound_extractor.get_sound_type())
                with open(sound_file, 'wb') as file:
                    file.write(sound)
                done[mylist_id].append(video_id)
                with open(dot_gazeru, 'w') as file:
                    file.write(json.dumps(done))
