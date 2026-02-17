import asyncio

from src.content_functions.parser import Parser
import nodriver as uc

if __name__ == '__main__':
    parser = Parser()
    uc.loop().run_until_complete(parser.post_new_videos())
