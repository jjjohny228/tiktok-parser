from src.content_functions.parser import Parser
import zendriver as uc

if __name__ == '__main__':
    parser = Parser()
    uc.loop().run_until_complete(parser._search_videos())
