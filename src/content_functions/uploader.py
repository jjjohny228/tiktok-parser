from enum import Enum
import requests

from config import Config


class Platforms(str, Enum):
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"


class ApostolVideoUploader:
    """
    Class to upload video using Apostol api
    """
    def __init__(self, platform, channel_id, description, video_url):
        self.platform = platform
        self.channel_id = channel_id
        self.description = description
        self.video_url = video_url

    def upload_video(self):
        """
        Function to parse file and upload video to the platforms
        """
        try:
            if self.platform == Platforms.TIKTOK.value:
                self.__post_tiktok_video()
            elif self.platform == Platforms.YOUTUBE.value:
                valid_video_description = self.__cut_description_for_youtube_videos()
                self.__post_youtube_video(description=valid_video_description)
            else:
                raise ValueError('Platform not supported')
        except Exception as e:
            print('Error while posting videos', e)

    def __cut_description_for_youtube_videos(self) -> str:
        """
        Function cuts video description due to the YouTube limitation.
        Max description length is 100 characters.
        """
        if len(self.description) > 100:
            return self.description[-100:]
        return self.description

    def __post_tiktok_video(self):
        postiz_post_url = Config.POSTIZ_POST_VIDEOS_URL
        data = {
            "type": "now",
            "date": "2024-12-14T10:00:00.000Z",
            "tags": [],
            "shortLink": "true",
            "posts": [
                {
                    "integration": {
                        "id": self.channel_id
                    },
                    "value": [
                        {
                            "content": self.description,
                            "image": [
                                {
                                    "id": "string",
                                    "path": self.video_url
                                }
                            ]
                        }
                    ],
                    "settings": {
                        "__type": "tiktok",
                        "privacy_level": "PUBLIC_TO_EVERYONE", # After authorization, replace with PUBLIC_TO_EVERYONE, SELF_ONLY
                        "duet": "false",
                        "stitch": "false",
                        "comment": "true",
                        "autoAddMusic": "no",
                        "brand_content_toggle": "false",
                        "brand_organic_toggle": "false",
                        "content_posting_method": "DIRECT_POST"
                    }
                },
            ],
        }
        headers = {
            'Authorization': Config.POSTIZ_API_KEY,
            'Content-Type': 'application/json'
        }
        response = requests.post(postiz_post_url, json=data, headers=headers)
        print(response.json())

    def __post_youtube_video(self, description):
        postiz_post_url = Config.POSTIZ_POST_VIDEOS_URL
        video_title = description if len(description) > 2 else '   '
        shortened_video_title = video_title if len(video_title) < 90 else video_title[-90:]
        data = {
            "type": "now",
            "date": "2024-12-14T10:00:00.000Z",
            "tags": [],
            "shortLink": "true",
            "posts": [
                {
                    "integration": {
                        "id": self.channel_id
                    },
                    "value": [
                        {
                            "content": '',
                            "image": [
                                {
                                    "id": "string",
                                    "path": self.video_url
                                }
                            ]
                        }
                    ],
                    "settings": {
                        "__type": "youtube",
                        "title": shortened_video_title,
                        "type": "public",
                        "selfDeclaredMadeForKids": "no",
                    }
                },
            ],
        }
        headers = {
            'Authorization': Config.POSTIZ_API_KEY,
            'Content-Type': 'application/json'
        }
        response = requests.post(postiz_post_url, json=data, headers=headers)
        print(response.json())

