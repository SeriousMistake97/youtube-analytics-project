import json
import os
from googleapiclient.discovery import build

API_KEY: str = os.getenv("YT_API_KEY")


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        request = youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()
        print(json.dumps(request, indent=2, ensure_ascii=False))
