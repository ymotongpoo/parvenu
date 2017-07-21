from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException:
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
        pass

    def close(self):
        self.browser.close()


def main():
    handler = SBIHandler()
    result = handler.fetch_all()
    [print(r['url'], r['name']) for r in result]
    handler.close()


if __name__ == '__main__':
    main()
