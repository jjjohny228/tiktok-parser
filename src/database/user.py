from .models import Channel, Video


def get_tiktok_username(url):
    username = url.split('/')[-1]
    return username.replace('@', '')


def get_channel_by_url_or_none(channel_url: str) -> None:
    return Channel.get_or_none(Channel.url == channel_url)


def get_video_by_url_or_none(video_url: str) -> None:
    return Video.get_or_none(Video.url == video_url)


def create_channel_if_not_exist(channel_url: str) -> bool:
    if not get_channel_by_url_or_none(channel_url):
        channel_name = get_tiktok_username(channel_url)
        Channel.create(url=channel_url, name=channel_name)
        return True
    return False


def create_video_if_not_exist(video_url: str, channel_name: str):
    if not get_video_by_url_or_none(video_url):
        channel = Channel.get(Channel.name == channel_name)
        Video.create(url=video_url, channel=channel)


def get_channels_names() -> list:
    return Channel.select(Channel.name)
