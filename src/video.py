import json
import os
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """
    Получить id можно из адреса видео
    https://www.youtube.com/watch?v= или https://youtu.be/
    """
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url_video = f'https://youtu.be/{video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.video_title}"