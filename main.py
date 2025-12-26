import nodriver as uc
import time
from src.functions import search_channels, add_channel
from src.database.models import register_models


if __name__ == '__main__':
    register_models()
    for channel_url in ['https://www.tiktok.com/@finestfilm', 'https://www.tiktok.com/@kino1uv',
                        'https://www.tiktok.com/@vlaymeer']:
        add_channel(channel_url)
    uc.loop().run_until_complete(search_channels())


