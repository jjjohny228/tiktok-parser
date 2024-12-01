import asyncio
import requests
from bs4 import BeautifulSoup
import nodriver as uc

from src.database.user import get_video_by_url_or_none, get_channels_names, create_channel_if_not_exist, \
    create_video_if_not_exist


async def get_last_channel_videos(username: str, max_links_quantity: int) -> list:
    try:
        print(f"Initiating scrape for TikTok profile: @{username}")
        browser = await uc.start(headless=False)
        print("Browser started successfully")

        page = await browser.get(f"https://www.tiktok.com/@{username}")
        print("TikTok profile page loaded successfully")

        await asyncio.sleep(10)  # Wait for 10 seconds
        print("Waited for 10 seconds to allow content to load")

        html_content = await page.evaluate('document.documentElement.outerHTML')
        print(f"HTML content retrieved (length: {len(html_content)} characters)")

        soup = BeautifulSoup(html_content, 'html.parser')
        print("HTML content parsed with BeautifulSoup")

        videos = soup.find_all('div', {'data-e2e': 'user-post-item'})[:max_links_quantity]

        video_links = []
        for video in videos:
            video_links.append(video.find('a').get('href'))
        return video_links
    except Exception as e:
        print(f"An error occurred while scraping: {str(e)}")
        return None
    finally:
        if 'browser' in locals():
            browser.stop()
        print("Browser closed")


async def search_channels():
    channels = [channel.name for channel in get_channels_names()]
    print(channels)
    if not channels:
        print('You dont have any channels')
    print("Каналы", channels)
    for channel in channels:
        new_channel_videos = await get_last_channel_videos(channel, 10)
        for video in new_channel_videos:
            create_video_if_not_exist(video, channel)


def add_channel(url):
    create_channel_if_not_exist(url)
