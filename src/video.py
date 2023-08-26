from googleapiclient.discovery import build
import os


API_KEY: str = os.getenv("YT_API_KEY")


class Video:
    def __init__(self, video_id: str):
        try:
            self.video_id = video_id

            request = Video.get_service().videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id,
                key=API_KEY
            ).execute()

            self.name_video = request['items'][0]['snippet']['title']
            self.url_video = f"https://www.youtube.com/watch?v={self.video_id}&ab_channel={request['items'][0]['snippet']['channelTitle']}"
            self.view_count = request['items'][0]['statistics']['viewCount']
            self.like_count = request['items'][0]['statistics']['likeCount']
        except IndexError:
            print(f"Video with id {video_id} not found")
            self.name_video = None
            self.url_video = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.name_video

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id