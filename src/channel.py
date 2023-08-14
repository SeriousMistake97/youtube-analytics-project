import json
from googleapiclient.discovery import build
import os

API_KEY: str = os.getenv("YT_API_KEY")


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        youtube = Channel.get_service()

        request = youtube.channels().list(
            part='snippet,statistics',
            id=self.__channel_id
        ).execute()

        self.title = request['items'][0]['snippet']['title']
        self.description = request['items'][0]['snippet']['description']
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        self.subscriber_count = int(request['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(request['items'][0]['statistics']['videoCount'])
        self.view_count = int(request['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # youtube = build('youtube', 'v3', developerKey=API_KEY)
        youtube = Channel.get_service()

        request = youtube.channels().list(
            part='snippet,statistics',
            id=self.__channel_id
        ).execute()
        print(json.dumps(request, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Геттер для атрибута youtube
        """
        return cls.youtube

    def to_json(self, path: str):
        """
        Выгрузка экземпляра класса в json
        """

        json_instance = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(path, 'w') as file:
            json.dump(json_instance, file, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id
