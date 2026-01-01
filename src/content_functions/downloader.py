import os
import re
import time
from http.client import IncompleteRead

import requests
from config import Config
from dotenv import load_dotenv

load_dotenv()


class VideoDownloader:
    rapid_api_key = Config.RAPIDAPI_KEY
    targets = ('tiktok', 'instagram', 'youtube')

    def __init__(self, video_url, target_folder):
        self.video_url = video_url
        self.target_folder = target_folder
        self.video_download_link = None

    def _save_video(self, max_retries=5):
        filename = str(int(time.time())) + '.mp4'
        response = requests.get(self.video_download_link, stream=False, timeout=60)
        retries = 0
        while retries < max_retries:
            try:
                with open(os.path.join(self.target_folder, filename), 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8900):
                        file.write(chunk)
                retries = 0
                break
            except IncompleteRead as e:
                print(f"Incomplete read: {e}, retrying...")
                os.remove(os.path.join(self.target_folder, filename))
                retries += 1
        return f'{self.target_folder}/{filename}'

    def _extract_video_id(self):
        # Regular expression to match YouTube video and shorts URLs
        video_id_pattern = r"(?:v=|\/shorts\/|\/embed\/|\/v\/|\/e\/|watch\?v=|watch\?.+&v=)([^&=%\?]{11})"
        match = re.search(video_id_pattern, self.video_url)
        if match:
            return match.group(1)
        else:
            return None

    def _insta_download(self):
        payload = {
            "url": self.video_url,
        }
        headers = {
            'x-rapidapi-host': os.getenv('INSTA_API_HOST'),
            'x-rapidapi-key': self.rapid_api_key,
            'Content-Type': "application/x-www-form-urlencoded",
        }

        api = os.getenv('INSTA_API_URL')
        response = requests.post(api, data=payload, headers=headers).json()
        if 'url' in response:
            self.video_download_link = response['medias'][0]['url']
            video_description = response['title']
            filename = self._save_video()
            return filename, video_description
        else:
            return None, None

    def _youtube_download(self):
        video_id = self._extract_video_id()
        params = {
            "id": video_id,
            'hd': '1',
        }
        headers = {
            'x-rapidapi-host': os.getenv('YOUTUBE_RAPIDAPI_HOST'),
            'x-rapidapi-key': self.rapid_api_key
        }

        api = os.getenv('YOUTUBE_API_URL')
        response = requests.get(api, params=params, headers=headers).json()
        if 'formats' in response:
            self.video_download_link = response['formats'][0]['url']
            video_description = response['title']
            filename = self._save_video()
            return filename, video_description
        else:
            return None, None

    def _tiktok_download(self):
        params = {
            "url": self.video_url,
            'hd': '1',
        }
        headers = {
            'x-rapidapi-host': os.getenv('TIKTOK_RAPIDAPI_HOST'),
            'x-rapidapi-key': self.rapid_api_key
        }

        api = os.getenv('TIKTOK_API_URL')
        response = requests.get(api, params=params, headers=headers).json()
        if 'data' in response:
            self.video_download_link = response['data']['hdplay']
            video_description = response['data']['title']
            filename = self._save_video()
            return filename, video_description
        else:
            return None, None

    def download(self):
        for target in self.targets:
            if target in self.video_url:
                if target == 'instagram':
                    filename, video_description = self._insta_download()
                elif target == 'youtube':
                    filename, video_description = self._youtube_download()
                elif target == 'tiktok':
                    filename, video_description = self._tiktok_download()

                if filename is None and video_description is None:
                    raise ValueError('Download failed. There is no url in response')
                return filename, video_description
        raise ValueError('Invalid link')
