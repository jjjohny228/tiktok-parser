import asyncio
from datetime import datetime, timedelta
from typing import Union

from bs4 import BeautifulSoup
import zendriver as uc

from config import Config
from src.content_functions.editor import post_video_from_source_channel
from src.database.models import Video, Channel
from src.database.user import create_video_if_not_exist, get_all_channels, get_target_by_channel, \
    update_last_video_published_time
from src.handlers.user.user import Utils
from src.utils import logger

_parser_lock = asyncio.Lock()

BROWSER_STOP_TIMEOUT = 30


class Parser:
    """
    Class to parse new videos in TikTok
    """
    MAX_LINKS_PER_CHANNEL = Config.MAX_LINKS_PER_CHANNEL

    def __init__(self):
        self.browser = None

    async def post_new_videos(self):
        """
        Excepts new videos and their source channel.
        Post videos to the target channel
        """
        new_videos = await self._search_videos()
        for video in new_videos:
            source_channel = video.get('source_channel')
            video_object = video.get('new_video')
            target = get_target_by_channel(source_channel)
            # Check if last published video time was more than 1 hours ago
            if not target.last_video_published_time or datetime.now() - target.last_video_published_time >= timedelta(
                    hours=1):
                post_video_from_source_channel(video_object.url, target.channel_apostol_id, target.platform)
                await Utils.send_posted_video_message(target.target_channel_url)
                update_last_video_published_time(datetime.now(), target.id)
                logger.success(f'New video added to channel {source_channel.name}')

    async def get_last_channel_videos(self, username: str) -> list:
        """
        Returns last channel videos
        """
        async with _parser_lock:
            try:
                self.browser = await uc.start(headless=True, sandbox=False)
                page = await self.browser.get(f"https://www.tiktok.com/@{username}")
                if page is None:
                    logger.warning(f"Browser returned None for {username}")
                    return []

                await asyncio.sleep(15)

                html_content = await page.evaluate('document.documentElement.outerHTML')
                if html_content is None:
                    logger.warning(f"Page evaluate returned None for {username}")
                    return []

                soup = BeautifulSoup(html_content, 'html.parser')
                new_videos = soup.find_all('div', {'data-e2e': 'user-post-item'})[:self.MAX_LINKS_PER_CHANNEL]
                if not new_videos:
                    logger.info(f"Skip channel {username}: no videos scraped")
                    return []

                video_links = []
                for video in new_videos:
                    link_el = video.find('a')
                    if link_el is None:
                        continue
                    href = link_el.get('href')
                    if href:
                        video_links.append(href)
                return video_links
            except Exception as e:
                logger.error(f"An error occurred while scraping: {str(e)}")
                return []
            finally:
                await self._close_browser()

    async def fetch_channel_videos(self, username: str) -> list[str]:
        """Fetches last videos for one channel (browser open/close inside get_last_channel_videos)."""
        return await self.get_last_channel_videos(username)

    async def _close_browser(self) -> None:
        """Guaranteed to close the browser with a timeout. Call in finally."""
        browser = self.browser
        self.browser = None
        if browser is None:
            return
        try:
            await asyncio.sleep(1)
            if getattr(browser, "connection", None) is None:
                logger.warning("Browser connection is None, skipping stop()")
                return
            stop_result = browser.stop()
            if asyncio.iscoroutine(stop_result):
                await asyncio.wait_for(stop_result, timeout=BROWSER_STOP_TIMEOUT)
            logger.info("Browser stopped successfully")
        except asyncio.TimeoutError:
            logger.error("Browser stop() timed out — process may still be running")
        except Exception as e:
            logger.error(f"Failed to stop browser: {e}")

    async def _search_videos(self) -> list[dict[str, Union[Channel, Video]]]:
        """
        Gets all channels from database and check do they have new videos.
        """
        channels = get_all_channels() or []
        new_videos = []
        if not channels:
            logger.info('You dont have any channels')
        try:
            for channel in channels:
                new_channel_videos = await self.get_last_channel_videos(channel.name)
                for video in new_channel_videos:
                    new_video = create_video_if_not_exist(video, channel)
                    if new_video:
                        new_videos.append({'source_channel': channel, 'new_video': new_video})
            return new_videos
        except Exception:
            logger.exception("Error raised during video parsing")
            return []


