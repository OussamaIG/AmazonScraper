import scrapy
import json

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s?k=playstation'  # Replace with your desired search URL
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # Add a delay to prevent blocking
        'RETRY_TIMES': 5,  # Number of retry attempts for failed requests
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.results = []

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Select the products on the search results page
        products = response.xpath('//div[@data-component-type="s-search-result"]')

        for product in products:
            # Extract product details
            title = product.xpath('.//h2/a/span/text()').get()
            price_whole = product.xpath('.//span[@class="a-price-whole"]/text()').get()
            price_fraction = product.xpath('.//span[@class="a-price-fraction"]/text()').get()
            rating = product.xpath('.//span[@class="a-icon-alt"]/text()').get()

            # Combine whole and fractional price if available
            price = f"{price_whole}.{price_fraction}" if price_whole and price_fraction else None

            # Store the extracted data in the results list
            self.results.append({
                'title': title,
                'price': price,
                'rating': rating,
            })

        # Handle pagination (optional)
        next_page = response.xpath('//li[@class="a-last"]/a/@href').get()
        if next_page:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            yield response.follow(next_page, headers=headers, callback=self.parse)
        else:
            # Save the results to a JSON file when finished
            self.save_to_json()

    def save_to_json(self):
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)
