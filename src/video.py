import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Video:
    """Класс для видео"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        self.video = Video.youtube.videos().list(id=self.__video_id, part='snippet, statistics, contentDetails').execute()
        self.title = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.__video_id
        self.like_count = self.video['items'][0]['statistics']['likeCount']
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.duration = self.video['items'][0]['contentDetails']['duration']
        self.url_short = 'https://youtu.be/' + self.__video_id

    def __str__(self):
        return f'{self.title}'

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id, playlist_id) -> None:
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
