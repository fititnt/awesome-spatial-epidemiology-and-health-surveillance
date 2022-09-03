from scrapy_playwright.page import PageMethod
import scrapy

# @see https://github.com/scrapy-plugins/scrapy-playwright

# pip install scrapy-playwright
# scrapy shell 'https://apps.who.int/whocc/Search.aspx'
# scrapy shell 'https://apps.who.int/whocc/Search.aspx'
#    response.css('select option[value=cc_region]').get()

#    from scrapy import FormRequest
# fetch(FormRequest('https://apps.who.int/whocc/Search.aspx', formdata={'ctl00$ContentPlaceHolder1$DropDownList1':'cc_region'}))


# scrapy crawl whocc
# scrapy fetch --nolog https://apps.who.int/whocc/Search.aspx > response.html

class WHOCCSpider(scrapy.Spider):
    name = "whocc"

    def start_requests(self):
        urls = [
            'https://apps.who.int/whocc/Search.aspx',
        ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
        for url in urls:
            yield scrapy.FormRequest(
                url=url,
                formdata={
                    'ctl00_ContentPlaceHolder1_DropDownList1': 'cc_region',
                    # 'ctl00$ContentPlaceHolder1$criteriaValue_1': 'AFRO'
                },
                callback=self.parse
            )

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'whocc-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


class AwesomeSpider(scrapy.Spider):
    name = "whocc_v2"

    def start_requests(self):
        # GET request
        yield scrapy.Request("https://httpbin.org/get", meta={"playwright": True})
        # POST request
        yield scrapy.FormRequest(
            url="https://httpbin.org/post",
            formdata={"foo": "bar"},
            meta={"playwright": True},
        )

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        yield {"url": response.url}

        page = response.url.split("/")[-2]
        filename = f'whocc-v2-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


class Awesome3Spider(scrapy.Spider):
    name = "whocc_v3"

    _start_url = 'https://apps.who.int/whocc/Search.aspx'

    def start_requests(self):
        # GET request
        yield scrapy.Request(
            self._start_url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod(
                        "screenshot",
                        path=self.name + "_initial.png",
                        full_page=True),
                ],
            }
        )
        # # POST request
        # yield scrapy.FormRequest(
        #     url="https://httpbin.org/post",
        #     formdata={"foo": "bar"},
        #     meta={"playwright": True},
        # )

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        yield {"url": response.url}

        page = response.url.split("/")[-2]
        filename = f'whocc-v3-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
