#    Copyright 2017 Yoshi Yamaguchi
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from time import sleep
from urllib.parse import urlparse, parse_qs

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from handler.handler import InvestmentTrustSiteHandler

class RakutenHandler(InvestmentTrustSiteHandler):
    """ RakutenHandler is a handler for Rakuten
    """

    def __init__(self):
        self.baseurl = "https://www.rakuten-sec.co.jp/web/fund/find/search/result.html"
        super().__init__(self.baseurl)

    def fetch_all(self):
        result = []

        select = Select(self.browser.find_element_by_id('recsperpage'))
        select.select_by_value('80')
        sleep(2)

        elems = self.browser.find_elements_by_xpath('//div[@id="table1"]//th[not(contains(@class, "align-C"))]')
        for e in elems:
            a = e.find_elements_by_tag_name('a')[0]
            result.append(
                {
                    'url': a.get_attribute('href'),
                    'name': a.text.strip(),
                }
            )

        parsed = urlparse(self.browser.current_url)
        query = parse_qs(parsed.query)
        page_num = int(query['pg'][0])

        while(True):
            try:
                pagers = self.browser.find_elements_by_xpath('//ul[@class="list-pager"]/li/a')
                pager = pagers[2]
                pager.click()

                parsed = urlparse(self.browser.current_url)
                query = parse_qs(parsed.query)
                cur_page_num = int(query['pg'][0])
                if (page_num >= cur_page_num):
                    break
                page_num = cur_page_num
                sleep(5)

                elems = self.browser.find_elements_by_xpath('//div[@id="table1"]//th[not(contains(@class, "align-C"))]')
                for e in elems:
                    a = e.find_elements_by_tag_name('a')[0]
                    result.append(
                        {
                            'url': a.get_attribute('href'),
                            'name': a.text.strip(),
                        }
                    )
            except NoSuchElementException:
                break

        return result

    def open_and_fetch_detail(self, url):
        self.browser.get(url)
        sleep(1)
        result = {}

        elem = self.browser.find_element_by_css_selector('h1.fund-name')
        name = elem.text.strip()                    # 商品名

        tables = self.browser.find_elements_by_css_selector('table.tbl-data-01')
        elems = tables[1].find_elements_by_tag_name('td')
        investment_manager = elems[0].text.strip()  # 運用会社
        net_asset = elems[1].text.strip()           # 純資産
        category = elems[2].text.strip()            # 楽天証券カテゴリ


        return {
            'name': name,
            'investment_manager': investment_manager,
            'category': category,
            'net_asset': net_asset,
        }


