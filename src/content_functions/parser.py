import asyncio
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import nodriver as uc

from config import Config
from src.content_functions.editor import post_video_from_source_channel
from src.database.user import create_video_if_not_exist, get_all_channels, get_target_by_channel, \
    update_last_video_published_time
from src.utils import logger


class Parser:
    """
    Class to parse new videos in TikTok
    """
    MAX_LINKS_PER_CHANNEL = Config.MAX_LINKS_PER_CHANNEL

    def __init__(self):
        self.browser = None

    async def search_videos(self):
        """
        Gets all channels from database and check do they have new videos
        """
        from src.handlers.user.user import Utils

        channels = get_all_channels()
        if not channels:
            logger.info('You dont have any channels')
        try:
            self.browser = await uc.start(headless=False)
            for channel in channels:
                new_channel_videos = await self.get_last_channel_videos(channel.name)
                for video in new_channel_videos:
                    is_new_video = create_video_if_not_exist(video, channel)
                    if is_new_video:
                        target = get_target_by_channel(channel)
                        # Check if last published video time was more than 2 hours ago
                        if not target.last_video_published_time or datetime.now() - target.last_video_published_time >= timedelta(hours=2):
                            post_video_from_source_channel(video, target.channel_apostol_id, target.platform)
                            await Utils.send_posted_video_message(target.target_channel_url)
                            update_last_video_published_time(datetime.now(), target.id)
                            logger.success(f'New video added to channel {channel.name}')
        finally:
            if self.browser:
                await self.browser.stop()

    async def get_last_channel_videos(self, username: str) -> list:
        """
        Returns last channel videos
        """
        try:
            if not self.browser:
                logger.error("Browser not initialized")
                return []

            page = await self.browser.get(f"https://www.tiktok.com/@{username}")

            await asyncio.sleep(10)  # Wait for 10 seconds

            html_content = await page.evaluate('document.documentElement.outerHTML')

            soup = BeautifulSoup(html_content, 'html.parser')

            new_videos = soup.find_all('div', {'data-e2e': 'user-post-item'})[:self.MAX_LINKS_PER_CHANNEL]
            if not new_videos:
                logger.info(f"Skip channel {username}: no videos scraped")
                return []

            video_links = []
            for video in new_videos:
                video_url = video.find('a').get('href')
                video_links.append(video_url)
            return video_links
        except Exception as e:
            logger.error(f"An error occurred while scraping: {str(e)}")
            return []

