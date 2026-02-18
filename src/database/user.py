from datetime import datetime

from .models import Channel, Video, Target, User


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


def create_video_if_not_exist(video_url: str, channel: Channel) -> Video | None:
    if not get_video_by_url_or_none(video_url):
        video = Video.create(url=video_url, channel=channel)
        return video
    return None


def create_target_if_not_exist(source_channel_url: str, target_channel_url: str, channel_apostol_id: str) -> Target | None:
    source_channel = Channel.get(url=source_channel_url)
    target = Target.get_or_none(Target.target_channel_url==target_channel_url, Target.source_channel==source_channel)
    if not target:
        new_target = Target.create(source_channel=source_channel,
                      target_channel_url=target_channel_url,
                      channel_apostol_id=channel_apostol_id)
        return new_target



def get_all_channels() -> list:
    return Channel.select()


def create_user_if_not_exist(username: str, first_name: str, last_name: str, telegram_id: int) -> bool:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(username=username, first_name=first_name, last_name=last_name, telegram_id=telegram_id)
        return True
    return False


def get_user_by_telegram_id_or_none(telegram_id: int) -> None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_all_targets():
    return (
        Target
        .select(Target.id, Target.target_channel_url, Channel.url)
        .join(Channel)
    )


def get_target_by_id(target_id: str) -> Target | None:
    return Target.get_or_none(Target.id == int(target_id))


def get_target_by_channel(channel: Channel) -> Target | None:
    return Target.get(Target.source_channel == channel)


def delete_target_by_id(target_id: int) -> None:
    """Deleted target, source channel and all videos that were parsed from this channel"""
    target = Target.get_or_none(Target.id == target_id)
    if not target:
        return

    target.source_channel.delete_instance()


def update_last_video_published_time(new_time: datetime, target_id: int) -> None:
    Target.update(last_video_published_time=new_time).where(Target.id==target_id).execute()



