from scrapy import Selector
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


class TgstatExtractor:

    def __init__(self):
        # self.channel_id = channel_id
        # self.channel_id_pattern = "[name='channel_id']" + "::attr(value)"
        self.tgstat_url = "https://www.betforward.com/#/sport/?type=1&sport=1&region=2340001&competition=3013&game=16534757"
        # self.info_pattern = "[class='columns large-2 medium-4 small-6 margin-bottom15']"
        self.get_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        # self.api_endpoint = 'https://ir.tgstat.com/channels/chart-data'

    def convert_html_text(self, html_text):
        if html_text.startswith('http'):
            return html_text
        soup = BeautifulSoup(html_text, "lxml")
        for script in soup(['script', 'style']):
            script.extract()
        for script in soup.find_all('script'):
            script.extract()
        for script in soup.find_all('style'):
            script.extract()
        for tag in soup.find_all(True):
            tag.attr = {}
        plain_text = soup.get_text().strip()
        return plain_text

    def extract_info(self):
        tgstat_info = {}
        response = requests.get(self.tgstat_url, auth=HTTPBasicAuth('test', 'testpass'),
                                headers=self.get_header, verify=False, timeout=60).content
        selector = Selector(text=response)
        selected_elements = selector.css(self.info_pattern).getall()
        element_list = []
        for element in selected_elements:
            element = self.convert_html_text(element).split('\n')[0].strip()
            element_list.append(element)

        channel_id_int = selector.css(self.channel_id_pattern).extract_first()

        tgstat_info["members"] = element_list[0]
        tgstat_info["average_post_reach"] = element_list[1]
        tgstat_info["daily_reach"] = element_list[2]
        tgstat_info["posts_per_day"] = element_list[3]
        tgstat_info["ERR_percentage"] = element_list[4]
        tgstat_info["citation_index"] = element_list[5]
        tgstat_info["channel_id_int"] = channel_id_int
        return tgstat_info

    def extract_chart(self, url, request_payload):
        return requests.post(url, data=request_payload).text


if __name__ == '__main__':
    # tg = TgstatExtractor('gizmiztel')
    # print(tg.extract_info())
    # url = tg.api_endpoint
    # info = tg.extract_info()
    # request_payload = {'id': info.get('channel_id_int', None),
    #                    'metric': 'views_per_post',
    #                    'period': 'days',
    #                    'dateRangeMin': '2020-06-05',
    #                    'dateRangeMax': '2020-06-19'}
    # print(tg.extract_chart(url=url, request_payload=request_payload))
    tg = TgstatExtractor()
    tg.extract_info()
