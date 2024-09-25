from .models import Channel, Video


def get_channel_by_url_or_none(channel_url: str) -> None:
    return Channel.get_or_none(Channel.url == channel_url)


def get_video_by_url_or_none(video_url: str) -> None:
    return Video.get_or_none(Video.url == video_url)


def create_channel_if_not_exist(channel_url: str) -> bool:
    if not get_channel_by_url_or_none(channel_url):
        Channel.create(url=channel_url)
        return True
    return False


def create_video_if_not_exist(video_url: str) -> bool:
    if not get_video_by_url_or_none(video_url):
        Video.create(url=video_url)
        return True
    return False


def get_channels_urls() -> list:
    return Channel.select(Channel.url).order_by(Channel.id.desc())