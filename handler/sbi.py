""" for SBI
"""
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

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from handler.handler import InvestmentTrustSiteHandler


class SBIHandler(InvestmentTrustSiteHandler):
    """ SBIHandler is a handler for SBI
    """

    def __init__(self):
        self.baseurl = "https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch.do"
        super().__init__(self.baseurl)

    def fetch_all(self):
        result = []

        select = Select(self.browser.find_element_by_id('pageRowsInput'))
        select.select_by_value('100')
        sleep(2)

        elems = self.browser.find_elements_by_class_name("fundDetail")
        for e in elems:
            result.append(
                {
                    'url': e.get_attribute('href'),
                    'name': e.text,
                }
            )

        while(True):
            try:
                pager = self.browser.find_element_by_link_text('次へ→')
                pager.click()
                sleep(5)

                elems = self.browser.find_elements_by_class_name('fundDetail')
                for e in elems:
                    result.append(
                        {
                            'url': e.get_attribute('href'),
                            'name': e.text,
                        }
                    )
            except NoSuchElementException:
                break;

        return result

    def open_and_fetch_detail(self, url):
        """ open_and_fetch_detail open url in browser and fetch
        investment trust fund detailed data from the page

        :param url str: URL of the page
        :rtype: fund data
        """

        self.browser.get(url)
        sleep(2)
        result = {}
        
        elems = self.browser.find_elements_by_tag_name('h3')
        name = elems[0].text               # 商品名

        elems = self.browser.find_elements_by_css_selector('.floatL .fl01')
        morning_star_category = elems[3].text  # モーニングスターカテゴリ

        elems = self.browser.find_elements_by_css_selector('table.md-l-table-01.has_tooltip.col1.md-l-utl-mt10')
        elems = elems[0].find_elements_by_tag_name('tr')
        strategy = elems[1].text            # 運用方針
        benchmark = elems[3].text           # ベンチマーク
        category = elems[5].text            # 商品分類
        association_code = elems[7].text    # 協会コード
        buying_commition = elems[9].find_elements_by_class_name('active')[0].text.strip() # 買付手数料
        custodian_fee = elems[12].text      # 信託報酬
        assets_retained = elems[14].text    # 信託財産留保額
        back_end_load = elems[16].text      # 解約手数料
        closing_date = elems[22].text       # 決算日
        closing_frequency = elems[24].text  # 決算頻度
        start_date = elems[40].text         # 設定日

        elems = self.browser.find_elements_by_css_selector('table.md-l-table-01.has_tooltip.lower')
        elems = elems[0].find_elements_by_tag_name('td')
        net_asset = elems[0].text           # 純資産

        elem = self.browser.find_element_by_link_text('目論見書')
        prospectus = elem.get_attribute('href')

        return {
            'name': name,
            'url': url,
            'morning_star_category': morning_star_category,
            'strategy': strategy,
            'benchmark': benchmark,
            'category': category,
            'association_code': association_code,
            'buying_commition': buying_commition,
            'custodian_fee': custodian_fee,
            'assets_retained': assets_retained,
            'back_end_load': back_end_load,
            'closing_date': closing_date,
            'closing_frequency': closing_frequency,
            'start_date': start_date,
            'net_asset': net_asset,
            'prospectus': prospectus,
        }
