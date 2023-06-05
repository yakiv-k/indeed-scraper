import scrapy
from urllib.parse import urlencode
from pathlib import Path
from jobSpider.items import JobspiderItem
import requests


API_KEY = "34b9d900-bab2-4fca-b610-58cd39da21aa"


def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url }
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class JobSpider(scrapy.Spider):
    name = "jobSpider"

    def start_requests(self):
        start_url = "https://ca.indeed.com/jobs?q=software%20developer&l=Toronto%2C%20ON&from=searchOnHP"
        
        yield scrapy.Request(url=get_scrapeops_url(start_url), callback=self.parse)

    def parse(self, response):
        
        filename = f"job-titles.html"
        Path(filename).write_bytes(response.body)
        for job in response.css("td.resultContent"):
            yield {
                "title": job.css("a.jcs-JobTitle span::text").get(),
                "company": job.css("span.companyName::text").get()
                # 'description': job.css('div.jobsearch-jobDescriptionText div div[2] ul li::text').get()
            }
