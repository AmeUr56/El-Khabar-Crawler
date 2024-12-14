import scrapy
from elkhabar_crawler.items import ArticleItem

class ElkhabarSpiderSpider(scrapy.Spider):
    name = "elkhabar_spider"
    allowed_domains = ["www.elkhabar.com"]
    start_urls = ["https://www.elkhabar.com/press/category/28/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D9%88%D8%B7%D9%86/"]

    def parse(self, response):
        page = response.xpath("//main//div[@class='row']//div[@id='category28']")
        # Get Articles in current page
        articles = page.xpath("div[@class='row'][1]//div[contains(@class,'col-md')]")

        # Traverse to the page of each article in current page
        for article in articles:
            rel_article_url = article.xpath(".//a/@href").get()
            if rel_article_url is None:
                continue
            yield scrapy.Request(response.urljoin(rel_article_url),callback=self.parse_article)
        
        # Get next page url
        current_page_url = page.xpath("div[@class='row'][2]").xpath(".//a[@class='active']/@href").get()
        next_page_url = current_page_url[:-1] + str(int(current_page_url[-1])+1)
        # Traverse to next page after parsing current page's articles 
        yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)
        
    def parse_article(self,response):
        article_item = ArticleItem()
        
        page_data = response.xpath("//section[@class='home-blog mb-15']")
        section1 = page_data.xpath(".//div[@class='col-md-12']")[0]
        
        article_item['title'] = section1.xpath("h1/text()").get()
        article_item['author'] = section1.xpath(".//div[@class='blog-info']")[0].xpath(".//span/b/text()").get()
        article_item['number_readers'] = section1.xpath(".//strong/span/text()").get()
        article_item['publish_date'] = section1.xpath(".//div[@class='blog-info']")[1].xpath(".//span/text()").get()
        article_item['content'] = page_data.xpath("//div[@id='article_body_content']/p/text()").getall()
        
        yield article_item