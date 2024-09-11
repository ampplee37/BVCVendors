import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider

# Local imports
from contactscraper.spiders.contactspider import ContactSpider

# standard packages
import re
import logging
import os
from datetime import datetime, timezone, timedelta
import sys

# Twisted
from twisted.internet import reactor, defer
from urllib.parse import urlparse

# tld
import tldextract

class Controller:
    def __init__(self, starting_urls, scrape_numbers=True, scrape_emails=True,
                 region="US", keywords=None, max_results=False):

        # Ensure the .logs directory exists
        os.makedirs('.logs', exist_ok=True)

        # Init logging
        start_time = datetime.now().timestamp()
        logging.basicConfig(filename=f'.logs/{start_time}.log', level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        # Init project with scrapy settings
        self.settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'contactscraper.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        self.settings.setmodule(settings_module_path, priority='project')

        # Extracting allowed domains from starting URLs
        self.allowed_domains = [urlparse(url).netloc for url in starting_urls]

        # Init instance variables
        self.starting_urls = starting_urls
        self.scrape_numbers = scrape_numbers
        self.scrape_emails = scrape_emails
        self.region = region
        self.keywords = [kw.lower() for kw in keywords] if keywords else []
        self.max_results = max_results

        logging.info("Controller initialized with keywords: %s", self.keywords)

    def scrape(self):
        configure_logging()
        runner = CrawlerRunner(self.settings)
        deferred = runner.crawl(ContactSpider, 
                               start_urls=self.starting_urls,
                               allowed_domains=self.allowed_domains,
                               scrape_numbers=self.scrape_numbers,
                               scrape_emails=self.scrape_emails,
                               region=self.region,
                               keywords=self.keywords,
                               max_results=self.max_results)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()