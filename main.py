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

from csv import DictWriter
from time import sleep

from handler.sbi import SBIHandler

def dump(filepath, data):
    """ dump write down all data into filepath as csv
    :param filepath str: CSV target filepath
    :param data list: list of dict data
    """
    with open(filepath, 'w') as f:
        writer = DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    handler = SBIHandler()
    try:
        all_items = handler.fetch_all()
        results = []
        for i in all_items:
            result = handler.open_and_fetch_detail(i['url'])
            results.append(result)
            sleep(3)

        dump("sbi.csv", results)          
    except AttributeError as e:
        raise e
    except IndexError as e:
        raise e
    finally:
        handler.close()


if __name__ == '__main__':
    main()
