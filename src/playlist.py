import datetime
import os
import isodate

from googleapiclient.discovery import build

from src.video import Video

api_key: str = os.getenv('YT_API_KEY')


class PlayList:
    """Класс для плейлиста"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.__playlist_id = playlist_id
        self.playlist = PlayList.youtube.playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.__playlist_id
        self.items = PlayList.youtube.playlistItems().list(playlistId=self.__playlist_id, part='snippet').execute()
        self.__total_duration = datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        for item in self.items['items']:
            self.__total_duration += isodate.parse_duration(Video(item['snippet']['resourceId']['videoId']).duration)

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self):
        like_list = []
        for item in self.items['items']:
            like_list.append(int(Video(item['snippet']['resourceId']['videoId']).like_count))
        for item in self.items['items']:
            if int(Video(item['snippet']['resourceId']['videoId']).like_count) == max(like_list):
                return Video(item['snippet']['resourceId']['videoId']).url_short
