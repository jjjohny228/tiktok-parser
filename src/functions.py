import requests
from bs4 import BeautifulSoup
from .database.user import get_video_by_url_or_none, get_channels_urls, create_channel_if_not_exist


def get_last_channel_videos(channel_url):
    response = requests.get(channel_url)
    print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    videos = soup.find_all('div', class_='user-post-item')[:10]
    print(len(videos))
    for video in videos:
        url = video.find('a').get('href')
        if get_video_by_url_or_none(url):
            print(url, 'Новое видео было добавлено в бд')


def search_channels():
    channels = [user.url for user in get_channels_urls()]
    if not channels:
        print('You dont have any channels')
    print("Каналы", channels)
    for channel in channels:
        get_last_channel_videos(channel)


def add_channel(url):
    create_channel_if_not_exist(url)
