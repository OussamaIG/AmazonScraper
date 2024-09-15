import scrapy
import json

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'RETRY_TIMES': 5,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    def __init__(self, search_query='', *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.search_query = search_query
        self.results = []
        self.start_urls = [
            f'https://www.amazon.com/s?k={self.search_query}'
        ]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        products = response.xpath('//div[@data-component-type="s-search-result"]')
        for product in products:
            title = product.xpath('.//h2/a/span/text()').get()
            price_whole = product.xpath('.//span[@class="a-price-whole"]/text()').get()
            price_fraction = product.xpath('.//span[@class="a-price-fraction"]/text()').get()
            rating = product.xpath('.//span[@class="a-icon-alt"]/text()').get()
            price = f"{price_whole}.{price_fraction}" if price_whole and price_fraction else None

            self.results.append({
                'title': title,
                'price': price,
                'rating': rating,
            })

        next_page = response.xpath('//li[@class="a-last"]/a/@href').get()
        if next_page:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            yield response.follow(next_page, headers=headers, callback=self.parse)
        else:
            self.save_to_json()

    def save_to_json(self):
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)
