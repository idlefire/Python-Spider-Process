import sys
from AlexaCallback import AlexaCallback
from threaded_crawler import threaded_crawler
Sleep_time = 1


def main(max_threads):
    scrape_callback = AlexaCallback()
    threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, max_threads=max_threads, timeout=60)


if __name__ == '__main__':

    max_threads = int(sys.argv[1])
    main(max_threads)
