import json
import os
import tldextract
from email_validator import validate_email, EmailNotValidError

class ContactscraperPipeline:

    def open_spider(self, spider):
        start_url = spider.start_urls[0]
        # Extract domain from URL
        extracted = tldextract.extract(start_url)
        domain_name = extracted.domain

        # Create output filename based on domain name
        self.output_filename = f"{domain_name}.json"

        self.file = open(self.output_filename, 'w')
        self.emails = set()
        self.numbers = set()
        self.keywords = set()
        self.url_map = {}

    def close_spider(self, spider):
        output = [{'url': url, 'emails': list(contact['emails']), 'numbers': list(contact['numbers']), 'keywords': list(contact['keywords'])} for url, contact in self.url_map.items()]
        self.file.write(json.dumps(output, indent=2))
        self.file.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        emails, numbers, keywords, url = item['emails'], item['numbers'], item['keywords'], item['url']

        if len(emails) == len(numbers) == len(keywords) == 0:
            return False

        if url not in self.url_map:
            self.url_map[url] = {'numbers': set(), 'emails': set(), 'keywords': set()}

        for email in emails:
            try:
                valid = validate_email(email)
                ascii_email = valid.ascii_email
                known_emails = self.url_map[url]['emails']
                if ascii_email not in known_emails:
                    known_emails.add(ascii_email)
            except EmailNotValidError:
                continue

        for number in numbers:
            self.url_map[url]['numbers'].add(number)

        for keyword in keywords:
            self.url_map[url]['keywords'].add(keyword)

        return True