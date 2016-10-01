import requests
import bs4
import django
import os
import datetime
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vegetable.settings")
django.setup()

from search.models import Vegetable, Record
from django.db import transaction


def crawler_veg_info():
    url = "http://www.114guoshu.com/hangqing/xinfadisc/"
    content = requests.get(url).text
    soup = bs4.BeautifulSoup(content, 'lxml')
    newest_report = soup.findAll('li', {'class': 'catlist_li'})[0]
    tag_a = newest_report.findChild('a')
    report_url = tag_a.get('href')
    report_content = requests.get(report_url).content
    report_content = report_content.decode('GBK')
    report_soup = bs4.BeautifulSoup(report_content, 'lxml')
    table = report_soup.findAll('tr')
    table_data = []
    for row in table[1:]:
        table_data.append(row.text.split())

    veg_info = filter(lambda x: len(x) == 6, table_data)
    return veg_info


def get_amount_from_price(price):
    price = ''.join([i for i in price if i in string.digits + '.'])
    price = float(price) * 100
    price = int(price)
    return price


def parse_veg_info(veg_info):
    rows = []
    for row in veg_info:
        veg = dict(
            veg_name=row[0],
            lowest_price=get_amount_from_price(row[1]),
            avg_price=get_amount_from_price(row[2]),
            highest_price=get_amount_from_price(row[3]),
            veg_type=row[4],
        )
        rows.append(veg)
    return rows


def get_veg_info_list():
    veg_info = crawler_veg_info()
    veg_list = parse_veg_info(veg_info)
    return veg_list


@transaction.atomic
def insert_records(veg_dict):
    for veg_dict in veg_dict:
        vegetable = Vegetable.objects.get_or_create(veg_name=veg_dict['veg_name'], veg_type=veg_dict['veg_type'])
        vegetable = vegetable[0]

        veg_dict.pop('veg_type')
        record = Record(vegetable=vegetable, **veg_dict)
        record.save()
        print(record, 'add success')


def main():
    veg_list = get_veg_info_list()
    insert_records(veg_list)


if __name__ == '__main__':
    main()
