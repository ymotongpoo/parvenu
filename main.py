from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class SBIHandler:
    URL = "https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch.do"

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.URL)

    def fetch_all(self):
        result = []

        elems = self.browser.find_elements_by_class_name("fundDetail")
        for e in elems:
            result.append(
                {
                    'url': e.get_attribute('href'),
                    'name': e.text,
                }
            )

        while(True):
            pager = self.browser.find_element_by_link_text('次へ→')
            if pager is None:
                break;
            pager.click()

            # marker = WebDriverWait(self.browser, 3).until(lambda x: x.find_element_by_class_name('md-l-table-01-fund'))
            # marker = WebDriverWait(self.browser, 5)
            sleep(5)

            elems = self.browser.find_elements_by_class_name('fundDetail')
            for e in elems:
                result.append(
                    {
                        'url': e.get_attribute('href'),
                        'name': e.text,
                    }
                )

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