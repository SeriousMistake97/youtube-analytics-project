import isodate
from datetime import timedelta

from src.video import Video


class PlayList(Video):

    def __init__(self, playlist_id):
        playlist = super().get_service().playlists().list(id=playlist_id, part="id, snippet").execute()

        self.playlist_id = playlist_id
        self._title = playlist['items'][0]['snippet']['title']
        self._url = f"https://www.youtube.com/playlist?list={playlist['items'][0]['id']}"

        # Получает список видео в плейлисте
        playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        # Получает все id видео из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Получает всю статистику видео в плейлисте
        self.video_response = super().get_service().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(video_ids)
                                                                  ).execute()

    @property
    def playlist_id(self):
        """Returns the playlist id"""
        return self.playlist_id

    @playlist_id.setter
    def playlist_id(self, value):
        """Sets the playlist id"""
        self._playlist_id = value

    @property
    def title(self):
        """Returns the playlist title"""
        return self._title

    @title.setter
    def title(self, value):
        """Sets the playlist title"""
        self._title = value

    @property
    def url(self):
        """Returns the playlist url"""
        return self._url

    @url.setter
    def url(self, value):
        """Sets the playlist url"""
        self._url = value

    @property
    def total_duration(self):
        """Returns the total duration of the playlist"""
        total_duration = 0

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration).seconds
            total_duration += duration

        return timedelta(seconds=total_duration)

    def show_best_video(self):
        """Returns the best video in the playlist"""
        max_likes: int = 0
        best_video: str = ""

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_likes:
                max_likes = int(video['statistics']['likeCount'])
                best_video = video["id"]
        return f"https://youtu.be/{best_video}"