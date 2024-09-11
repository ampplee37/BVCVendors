# Scrape for emails, phones, and keywords

from contactscraper.controller import Controller
import json
import tldextract

# Specify the starting URL once
starting_url = 'https://www.evolutepower.com/'

# Initialize the Controller with the starting URL
instance = Controller(starting_urls=[starting_url],
                      scrape_numbers=True,
                      scrape_emails=True,
                      region="US",
                      keywords=['Fast Chargers'],
                      max_results=5)

# Run the scrape
instance.scrape()

# Extract the domain from the starting URL to create the output filename dynamically
extracted = tldextract.extract(starting_url)
domain_name = extracted.domain

# Open the domain-specific output file and read its contents
with open(f'{domain_name}.json', 'r') as raw_output:
    data = raw_output.read()
    output = json.loads(data)

# Print the JSON data in a formatted manner
print(json.dumps(output, indent=2))