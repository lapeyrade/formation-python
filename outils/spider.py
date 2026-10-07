"""Spider de référence ; cible HTML locale fournie par le kit."""

import argparse

import scrapy
from scrapy.crawler import CrawlerProcess


class MachinesSpider(scrapy.Spider):
    name = "machines"

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [url]

    def parse(self, response):
        for carte in response.css("article.machine"):
            yield {
                "nom": carte.css("h2::text").get(),
                "ip": carte.css(".ip::text").get(),
                "site": carte.css(".site::text").get(),
            }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("sortie")
    args = parser.parse_args()
    process = CrawlerProcess(
        {
            "LOG_LEVEL": "WARNING",
            "TELNETCONSOLE_ENABLED": False,
            "ROBOTSTXT_OBEY": False,
            "DOWNLOAD_TIMEOUT": 5,
            "FEEDS": {args.sortie: {"format": "json", "encoding": "utf-8", "overwrite": True}},
        }
    )
    process.crawl(MachinesSpider, url=args.url)
    process.start()


if __name__ == "__main__":
    main()
