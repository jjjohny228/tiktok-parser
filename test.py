import asyncio

from src.content_functions.parser import Parser

if __name__ == '__main__':
    parser = Parser()
    asyncio.run(parser.search_videos())
