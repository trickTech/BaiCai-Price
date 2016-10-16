import requests
from bs4 import BeautifulSoup as bs
import django
import os
import datetime
import string
import logging
import time
import sys

logging.basicConfig(filename='crawler.log', level=logging.INFO)

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vegetable.settings")
django.setup()
from django.db import transaction

from search.models import (
    Item,
    ItemType,
    Record
)
from spider.const import (
    BASE_URL,
    SLEEP_TIME,
    INDEX_TYPE_MAPPER
)

CREATE_DATETIME = datetime.datetime.now()


def veg_spider(item_type, oldest_date=None):
    if oldest_date is None:
        oldest_date = datetime.datetime.now().date()
    if not isinstance(oldest_date, datetime.date):
        try:
            oldest_date = datetime.datetime.strptime(oldest_date, '%Y-%m-%d').date()
        except ValueError:
            raise Exception("Oldest_date not invalid Error")

    stop = False
    page = 1

    records = []

    while not stop:
        logger.info('crawling page {} start'.format(page))
        url = BASE_URL.format(item_type=item_type, page=page)
        try:
            raw_html = requests.get(url).text
        except requests.RequestException as exc:
            logging.warning(repr(exc))
            continue

        rows = parse_page(raw_html, item_type)

        for index, row in enumerate(rows):
            if row['recorded_at'] < oldest_date:
                rows = rows[:index]
                stop = True
                break

        records.extend(rows)
        logger.info('crawling page {} success'.format(page))
        page += 1

        time.sleep(SLEEP_TIME)

    return records

def store_date(rows):
    counter = 0
    for row in rows:
        item_type = ItemType.objects.get_or_create(type_name=row['item_type'], defaults={'created_at': CREATE_DATETIME})[0]
        item = Item.objects.get_or_create(item_name=row['item_name'], item_unit=row['unit'], item_type=item_type,
                                          defaults={'created_at': CREATE_DATETIME})[0]

        row.pop('item', None)
        row.pop('item_type', None)
        recorded_at = row.pop('recorded_at')
        record, result = Record.objects.get_or_create(item=item, recorded_at=recorded_at, defaults=row)
        counter += 1 if result else 0

    logging.info('add {} records successfully'.format(counter))


def parse_page(raw_html, item_type):
    """
    parse raw html
    :param raw_html:
    :param item_type:
    :return: list<dict>
    """

    def clean_date(row_dict):
        del row_dict['useless']
        row_dict['item'] = row_dict['item_name']
        row_dict['lowest_price'] = int(float(row_dict['lowest_price']) * 100)
        row_dict['avg_price'] = int(float(row_dict['avg_price']) * 100)
        row_dict['highest_price'] = int(float(row_dict['highest_price']) * 100)
        row_dict['item_type'] = INDEX_TYPE_MAPPER.get(item_type)
        try:
            row_dict['recorded_at'] = datetime.datetime.strptime(row_dict['recorded_at'], '%Y-%m-%d').date()
        except ValueError:
            raise Exception('Date format error')

        return row_dict

    soup = bs(raw_html)

    table = soup.find('table', {'class': 'hq_table'})
    trs = table.findAll('tr')
    rows_td = [i.findAll('td') for i in trs][1:]  # 去掉表头

    rows = []
    for row in rows_td:
        labels = ['item_name', 'lowest_price', 'avg_price', 'highest_price', 'useless', 'unit', 'recorded_at']
        row = [td.get_text() for td in row][:-1]  # 去掉最后一个无用的
        row = dict(zip(labels, row))
        row = clean_date(row)
        rows.append(row)

    return rows


def main(oldest_date=None):
    for i in INDEX_TYPE_MAPPER:
        records = veg_spider(i, oldest_date)
        store_date(records)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
