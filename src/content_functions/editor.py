import os
import subprocess
import requests

from config import Config

from src.content_functions.downloader import VideoDownloader
from src.content_functions.utils import get_video_duration
from src.content_functions.uploader import ApostolVideoUploader


def cut_last_second(video_path: str, result_folder: str) -> str:
    """
    Cuts last second of a video
    """
    video_duration = get_video_duration(video_path)
    trim_duration = video_duration - 1

    output_video = os.path.join(
        result_folder, f"trimmed_{os.path.basename(video_path)}"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-t", f"{trim_duration:.3f}",
        "-c", "copy",
        output_video,
    ]
    subprocess.run(cmd, check=True)

    os.remove(video_path)
    return output_video


def upload_video_file(video_path: str) -> str | None:
    """
    Function uploads file to postiz app using api and returns url
    """
    try:
        with open(video_path, 'rb') as f:
            files = {"file": ('filename', f, "video/mp4")}
            headers = {"Authorization": Config.POSTIZ_API_KEY}
            response = requests.post(
                Config.POSTIZ_UPLOAD_FILE_URL,
                headers=headers,
                files=files,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            if response.status_code == 429:
                print('Postiz limit was exceeded. Need to wait next hour.')
            return data.get('path')
    except Exception as e:
        print('During uploading to postiz exception raised', e)
    return None



def post_video_from_source_channel(video_url: str, target_channel_id: str, platform: str, ):
    """
    This function downloads video, trims it and post to YouTube
    """
    source_folder = Config.SOURCE_FOLDER
    result_folder = Config.RESULT_FOLDER
    video_file, video_description = VideoDownloader(video_url, source_folder).download()
    cutted_video = cut_last_second(video_file, result_folder)
    edited_video_url = upload_video_file(cutted_video)
    ApostolVideoUploader(platform, target_channel_id, video_description, edited_video_url).upload_video()
    os.remove(video_file)


if __name__ == '__main__':
    post_video_from_source_channel('https://www.tiktok.com/@tonito.rt/video/7588585185726319894?is_from_webapp=1&sender_device=pc',
                                   'cmiycbf580001qb6wfg71hnpg',
                                   'youtube'
                                   )
