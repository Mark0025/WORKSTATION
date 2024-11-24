import argparse
from app import YouTubeWisdomExtractor

def main():
    parser = argparse.ArgumentParser(description='YouTube Wisdom Extractor')
    parser.add_argument('url', help='YouTube video URL to process')
    
    args = parser.parse_args()
    
    extractor = YouTubeWisdomExtractor()
    extractor.process_video(args.url)

if __name__ == '__main__':
    main() 