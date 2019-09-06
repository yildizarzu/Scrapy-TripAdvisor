# -*- coding: utf-8 -*-
import scrapy
from ..items import ExampleItem
from scrapy import Request
from urlparse import urljoin
from urlparse import urlparse


class Example2Spider(scrapy.Spider):
    name = 'example2'
    start_urls = ['https://www.tripadvisor.com.tr/Restaurants-g297977-Bursa.html']

    def parse(self, response):
 
        for href in response.xpath("//div[@class='title']/a[@class='property_title']/@href"):
            url=response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath("//div[contains(@class, 'unified')]/a[contains(@class, 'next')]/@href")
        if next_page:
            url= response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
        
        
            

    def parse_page(self, response):
        item=ExampleItem()
        titleRestaurant=response.xpath("//div[contains(@class, 'restaurantName')]/h1/text()").extract()#Restoranın Adı

        address=response.xpath("//span[contains(@class, 'detailLinkText--co3ei')]/text()").extract()#Mekan Adresi

        state=response.xpath("//span[@class='extended-address']/text()").extract() #İlçe Adı

        city=response.xpath("//span[@class='locality']/text()").extract() #Şehir Adı

        country=response.xpath("//span[@class='country-name']/text()").extract() #Ülke Ad

        mobile=response.xpath("//span[contains(@class, 'mobile')]/text()").extract() #Telefon Numarası

        kitchenType=response.xpath("//div[@class='header_links']/a/text()")[1].extract().encode('utf8') #Mutfak Türü

        rating = response.xpath("//div[contains(@class, 'primaryRatingRow')]/span[contains(@class, 'RatingsOverviewCard')]/text()").extract()[0]  
        
        reviewTitles= response.xpath("//span[@class='noQuotes']/text()").extract()
        reviewTitle=reviewTitles[0].encode("utf8") #Yorum Başlığı

        contents = response.xpath('//div[@class="entry"]/p/text()').extract()
        content = contents[0].encode("utf-8") #Yorumlar

        item['titleRestaurant']=titleRestaurant
        item['address']=address
        item['state']=state
        item['city']=city
        item['country']=country
        item['mobile']=mobile
        item['kitchenType']=kitchenType
        item['rating']=rating
        item['reviewTitle']=reviewTitle
        item['content']=content
        
        yield item

