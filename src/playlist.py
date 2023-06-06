import json
import os

import isodate
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """Реализуйте класс `PlayList`, который инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
  - название плейлиста
  - ссылку на плейлист

- Реализуйте следующие методы класса `PlayList`
  - `total_duration` возвращает объект класса `datetime.timedelta`
  с суммарной длительность плейлиста (обращение как к свойству, использовать `@property`)
  - `show_best_video()` возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        playlists = youtube.playlists().list(id=playlist_id,
                                             part='snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        '''
        вывести длительности видеороликов из плейлиста
        docs: https://developers.google.com/youtube/v3/docs/videos/list
        '''
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_duration = 0
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += int(duration.total_seconds())
        return total_duration

    def show_best_video(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        url_best_video = []
        max_like_count = 0
        for video in video_response['items']:
            like_count: int = video['statistics']['likeCount']
            video_id = video['contentDetails']['videoId']
            if like_count > max_like_count:
                url_best_video = f'https://youtu.be/{video_id}'
        return url_best_video
