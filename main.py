from time import sleep
from csv import DictWriter

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait


class SBIHandler:
    URL = "https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch.do"

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.URL)

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
        self.browser.get(url)
        sleep(2)
        result = {}
        
        elems = self.browser.find_elements_by_tag_name('h3')
        name = elems[0].text               # 商品名

        elems = self.browser.find_elements_by_css_selector('.floatL .fl01')
        morning_star_category = elems[3].text  # モーニングスターカテゴリ

        elems = self.browser.find_elements_by_css_selector('.md-l-table-01 .has_tooltip .col1 .md-l-utl-mt10')
        elem = elems[0]
        elems = elem.find_elements_by_tag_name('tr')
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

        elems = self.browser.find_elements_by_css_selector('.md-l-table-01 .has_tooltip .lower')
        elem = elems[0]
        elems = elem.find_elements_by_tag_name('td')
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

    def close(self):
        self.browser.close()


def main():
    handler = SBIHandler()
    try:
        all_items = handler.fetch_all()
        results = []
        for i in all_items:
            result = handler.open_and_fetch_detail(i['url'])
            results.append(result)
            sleep(3)
        
        with open('data.tsv', 'w') as f:
            writer = DictWriter(f, fieldnames=results[0].keys())
            wrtier.writeheader()
            writer.writerows(results)
    except AttributeError as e:
        raise e
    finally:
        handler.close()


if __name__ == '__main__':
    main()
