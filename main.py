import nodriver as uc
from src.functions import search_channels, add_channel
from src.database.models import register_models


register_models()
uc.loop().run_until_complete(search_channels())


