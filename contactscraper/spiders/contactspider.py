import scrapy
import re
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy import signals
from pydispatch import dispatcher
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timezone
from contactscraper.items import ContactInfo
import phonenumbers as pn
from urllib.parse import urlparse

class ContactSpider(CrawlSpider):
    name = "contactspider"

    def __init__(self, *args, **kwargs):
        super(ContactSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.start_urls = kwargs.get('start_urls', [])
        self.scrape_numbers = kwargs.get('scrape_numbers', True)
        self.scrape_emails = kwargs.get('scrape_emails', True)
        self.region = kwargs.get('region', "US")
        self.keywords = kwargs.get('keywords', [])
        self.max_results = kwargs.get('max_results', False)
        self.seen_urls = set()

        # Get allowed domains from kwargs
        self.allowed_domains = kwargs.get('allowed_domains', [])

        # Define rules to exclude non-HTML file types
        self.rules = (
            Rule(
                LinkExtractor(
                    allow_domains=self.allowed_domains,
                    deny=(
                        r'\.jpg$', r'\.jpeg$', r'\.png$', r'\.gif$', r'\.bmp$', r'\.webp$', r'\.svg$',  # image files
                        r'\.pdf$', r'\.doc$', r'\.docx$', r'\.xls$', r'\.xlsx$', r'\.ppt$', r'\.pptx$',  # document files
                        r'\.mp3$', r'\.mp4$', r'\.avi$', r'\.mov$', r'\.wmv$', r'\.flv$', r'\.mkv$',  # video files
                        r'\.zip$', r'\.tar$', r'\.gz$', r'\.bz2$',  # compressed files
                        r'\.exe$', r'\.dmg$', r'\.iso$',  # executable files
                    )
                ),
                callback='parse_item',
                follow=True
            ),
        )
        super(ContactSpider, self)._compile_rules()

    def parse_item(self, response):
        # Check if content type is HTML
        if 'text/html' not in response.headers.get('Content-Type', '').decode('utf-8'):
            return

        contact_info = ContactInfo()
        contact_info['url'] = response.url
        html_text = str(response.text).lower()

        potential_numbers = [pn.format_number(match.number, pn.PhoneNumberFormat.E164) for match in pn.PhoneNumberMatcher(html_text, self.region)]
        potential_emails = re.findall(r'\w+@\w+\.\w+', html_text)

        keywords_found = [kw for kw in self.keywords if kw.lower() in html_text]

        if response.url not in self.seen_urls and \
                (len(potential_numbers) != 0 or len(potential_emails) != 0 or len(keywords_found) != 0):

            contact_info['emails'] = potential_emails if self.scrape_emails else []
            contact_info['numbers'] = potential_numbers if self.scrape_numbers else []
            contact_info['keywords'] = keywords_found  # Add keywords to the contact_info

            yield contact_info

    def spider_closed(self, spider):
        logging.info("Spider closed: %s", spider.name)