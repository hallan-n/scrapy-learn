import scrapy
from scrapy.http.response.html import HtmlResponse


class AosFatosSpider(scrapy.Spider):
    name = "aosfatos"
    start_urls = ["https://aosfatos.org/"]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//nav//ul/li/div/div/ul/li/a/@href").getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_category)

    def parse_category(self, response: HtmlResponse):
        news = response.xpath(
            "//a[@class='entry-item-card entry-content ']/@href"
        ).getall()
        for new_url in news:
            yield scrapy.Request(response.urljoin(new_url), callback=self.parse_new)

    def parse_new(self, response: HtmlResponse):
        title = response.xpath("//h1/text()").get()
        date = " ".join(
            response.xpath("//*[@class='publish-date']/text()").get().split()
        )
        quotes = response.xpath(
            "//article[@class='ck-article secondary-content entry-content']/blockquote/text()"
        ).get()
        if len(quotes) < 10:
            quotes = response.xpath(
                "//article[@class='ck-article secondary-content entry-content']/blockquote/p/text()"
            ).get()
        if len(quotes) < 10:
            quotes = response.xpath(
                "//article[@class='ck-article secondary-content entry-content']/p/text()"
            ).get()
        status_quotes = ""
        url = response.url
        yield {"title": title, "date": date, "quotes": quotes, "url": url}
