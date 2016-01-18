import os
import json
from config import Config
from nicovideo_api import NicovideoAPI
from sound_extractor import SoundExtractorFactory
from exception import *

class Gazeru:
    def __init__(self):
        self.config = Config()
        self.niconico = NicovideoAPI(self.config.get_user(), self.config.get_password())
        self.sound_extractor_factory = SoundExtractorFactory()
        self.dot_gazeru = '{0}/.gazeru'.format(self.config.get_directory())

    def get_mylists(self):
        return self.config.get_mylists()

    def set_account(self, user, password):
        self.config.set_user(user)
        self.config.set_password(password)
        self.niconico.login()
        return self

    def set_directory(self, directory):
        self.config.set_directory(directory)
        self.dot_gazeru = '{0}/.gazeru'.format(self.config.get_directory())
        return self

    def add_mylist(self, mylist_id):
        registerd_mylist_id_list = [mylist['id'] for mylist in self.config.get_mylists()]
        if mylist_id in registerd_mylist_id_list:
            raise AlreadyRegisteredMylistError()
        mylist_info = self.niconico.get_mylist_info(mylist_id)
        self.config.add_mylist({'id': mylist_info['id'], 'creator': mylist_info['creator'], 'title': mylist_info['title']})

    def pull(self):
        if not os.path.exists(self.dot_gazeru):
            self.create_dot_gazeru()
        mylists = self.config.get_mylists()
        all_mylist_info = {mylist['id']: self.niconico.get_mylist_info(mylist['id']) for mylist in mylists}
        all = {mylist_info['id']: mylist_info['video_list'] for mylist_id,mylist_info in all_mylist_info.items()}
        with open(self.dot_gazeru, 'r') as file:
            done = json.loads(file.read())
        not_yet_downloads = {mylist_id: [video_id for video_id in video_id_list if mylist_id not in done.keys() or video_id not in done[mylist_id]] for mylist_id,video_id_list in all.items()}
        for mylist_id,video_id_list in not_yet_downloads.items():
            for video_id in video_id_list:
                video_info, video = self.download_video(video_id)
                sound,sound_type = self.extract_sound(video, video_info)
                sound_file_path = '{0}/{1}'.format(self.config.get_directory(), all_mylist_info[mylist_id]['creator'])
                os.makedirs(sound_file_path, exist_ok=True)
                sound_file = '{0}/{1}.{2}'.format(sound_file_path, self.escape_slash(video_info['title']), sound_type)
                with open(sound_file, 'wb') as file:
                    file.write(sound)
                if mylist_id not in done.keys():
                    done[mylist_id] = []
                done[mylist_id].append(video_id)
                with open(self.dot_gazeru, 'w') as file:
                    file.write(json.dumps(done))

    def escape_slash(self, title):
        return title.replace("/", "／")

    def extract_sound(self, video, video_info):
        sound_extractor = self.sound_extractor_factory.build(video, video_info['movie_type'])
        return (sound_extractor.extract(video), sound_extractor.get_sound_type())

    def download_video(self, video_id):
        return (self.niconico.get_thumb_info(video_id), self.niconico.get_flv(video_id))

    def create_dot_gazeru(self):
        with open(self.dot_gazeru, 'w') as file:
            file.write(json.dumps({mylist['id']:[] for mylist in config.get_mylists()}))
        return self
