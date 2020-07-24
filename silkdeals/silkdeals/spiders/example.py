# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector


class ExampleSpider(scrapy.Spider):
    name = 'example'
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://duckduckgo.com',
            wait_time = 3,
            screenshot=True,
            callback=self.parse
        )

        

    def parse(self, response):
        img = response.meta['screenshot']

        with open('screenshot.png', 'wb') as f:
            f.write(img)

        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search_input.send_keys('Hello World')

        search_input.send_keys(Keys.ENTER)
        #driver.save_screenshot('enter.png')

        html = driver.page_source
        response_obj = Selector(text = html)


        result_links = response_obj.xpath("//div[@class='result__extras__url']/a")
        for link in result_links:
            yield {
                'URL': link.xpath(".//@href").get()
            }