import scrapy

class ContactInfo(scrapy.Item):
    url = scrapy.Field()
    numbers = scrapy.Field()
    emails = scrapy.Field()
    keywords = scrapy.Field()  # Add keywords field