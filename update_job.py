# coding: utf8
# describe: 每天定时将shopee_item更新的商品导入shopee_item_job表

import sys
import time
import argparse
sys.path.append('../..')
from lib.db import DB
from lib.lib import Tool

parser = argparse.ArgumentParser(description='shopee_item更新的商品导入shopee_item_job表.')
parser.add_argument(
    '-start',
    type=str, 
    help='导入范围开始时间 %Y-%m-%d %H:%M:%S'
)
parser.add_argument(
    '-end', 
    type=str,
    help='导入范围结束时间 %Y-%m-%d %H:%M:%S'
)

parser.add_argument(
    '-limit', 
    type=str,
    help='批次限制'
)

args = parser.parse_args()

def generate_shopee_item_job():
    day_start = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
    day_end = time.strftime("%Y-%m-%d 23:59:59", time.localtime())
    if args.start:
        day_start = args.start
    if args.end:
        day_end = args.end
    sql = """insert ignore into shopee_item_job (shop_id, item_id)
            select shop_id, item_id from shopee_item
            where update_time>='{}' and update_time<='{}' %s
            on duplicate key update deal_flag=0
        """.format(day_start, day_end)
    if args.limit:
        sql = sql % "limit {}".format(args.limit)
    try:
        DB(Tool.get_mysql_config('shopee_test')).execute(sql)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    generate_shopee_item_job()
