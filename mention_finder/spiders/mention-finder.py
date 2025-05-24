import scrapy

class MentionsSpider(scrapy.Spider):
    name = "mentions"
    allowed_domains = [
        # Allowed domains here
    ]
    keywords = [
        # Keywords to find in all pages scraped
    ]

    start_urls = [
        # Page to start the spider on
    ]

    def parse(self, response):
        for text in response.xpath("//body//*/text()"):
            content = text.get()
            if (
                any(keyword in content for keyword in self.keywords)
                # Exclude the following subdomains
                and not response.url.startswith("https://it")
                and not response.url.startswith("https://uwconnect")
            ):
                yield {
                    'url': response.url,
                    'mention': content.strip()
                }
        
        # Make sure the URL does not lead to a PDF file
        yield from response.follow_all(xpath="//a[contains(@href, 'http') and not(contains(@href, '.pdf'))]/@href", callback=self.parse)