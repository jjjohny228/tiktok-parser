from datetime import datetime

from .models import Channel, Video, Target, User


def extract_username_from_tiktok_url(url):
    username = url.split('/')[-1]
    return username.replace('@', '')


def create_channel_if_not_exist(channel_url: str) -> bool:
    channel_name = extract_username_from_tiktok_url(channel_url)
    channel, created = Channel.get_or_create(url=channel_url, name=channel_name)
    return created

def create_video_if_not_exist(video_url: str, channel: Channel) -> Video | None:
    video, created = Video.get_or_create(url=video_url, channel=channel)
    if created:
        return video
    return None


def create_target_if_not_exist(source_channel_url: str, target_channel_url: str, channel_apostol_id: str) -> Target | None:
    source_channel = Channel.get_or_none(Channel.url == source_channel_url)
    if not source_channel:
        return
    target, created = Target.get_or_create(source_channel=source_channel,
                                           target_channel_url=target_channel_url,
                                           channel_apostol_id=channel_apostol_id)
    if created:
        return target



def get_all_channels() -> list:
    return Channel.select()


def create_user_if_not_exist(username: str, first_name: str, last_name: str, telegram_id: int) -> bool:
    user, created = User.get_or_create(username=username, first_name=first_name, last_name=last_name,
                                       telegram_id=telegram_id)
    return created


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



