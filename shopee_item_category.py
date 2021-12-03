# coding: utf8

import time
import random
import requests

from copy import deepcopy

import sys
sys.path.append('../..')
from lib.lib import Tool
from lib.clickhouse import Clickhouse
from lib.db import DB

PROJECT = 'shopee_item_category'
log = Tool.get_logger("script_" + PROJECT)

class GetShopeeCatrgory:
    BATCH = 500

    def __init__(self, init_task=[]):
        self.db_table = 'shopee_item_category'
        self.request_queue = init_task
        self.cookie = {}
        self.mysql_key_map = {
            'cid': 0, 'parent_cid': 0, 'top_parent_cid': 0, 'name': '', 'lv1name': '', 'lv2name': '', 'lv3name': '', 
            'lv4name': '', 'lv1cid': 0, 'lv2cid': 0, 'lv3cid': 0, 'lv4cid': 0, 'is_parent': 0, 'level': 1, 
        }
        self.insert_queue = []

    def get_content(self, cid):
        if type(cid) is int:
            url = 'https://shopee.sg/api/v4/pages/get_sub_category_list?parent_catid={}'.format(cid)
        else:
            url = cid
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; TAS-AN00 Build/HUAWEITAS-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.2.0.1100 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        resp = requests.get(url, headers=headers, cookies=self.cookie)
        self.cookie = resp.cookies
        return resp.json()

    def deal_requests(self):
        if not self.request_queue:
            self.request_queue.append('https://shopee.sg/api/v4/pages/get_homepage_category_list')
        while (self.request_queue):
            count = len(self.request_queue)
            cid = self.request_queue.pop(0)
            print('Current task cid/queue count：{}/{}'.format(cid, count))
            # log.info('Current task cid/queue count：{}/{}'.format(cid, count))
            self.deal_data_by_request(self.get_content(cid))
            second = random.randint(1, 2)
            print('Sleep time：{} second'.format(second))
            # log.info('Sleep time：{} second'.format(second))
            time.sleep(second)

    def deal_data_by_request(self, content):
        category_list = content['data'].get('category_list', [])
        for category in category_list:
            # 任务队列添加新的cid任务
            if category['level'] < 2:
                self.request_queue.append(category['catid'])
            cat_info = deepcopy(self.mysql_key_map)
            cat_info['cid'] = int(category['catid'])
            cat_info['name'] = category['display_name']
            cat_info['parent_cid'] = int(category['parent_catid']) if category['parent_catid'] else 0
            cat_info['level'] = category['level']

            # 添加lvn信息
            cat_info['lv{}cid'.format(cat_info['level'])] = cat_info['cid']
            cat_info['lv{}name'.format(cat_info['level'])] = cat_info['name']
            if cat_info['parent_cid']:
                cat_info['lv{}cid'.format(int(cat_info['level'])-1)] = cat_info['parent_cid']
            self.insert_queue.append(cat_info)
        if len(self.insert_queue) >= self.BATCH/10 or not self.request_queue:
            if not self.insert_mysql():
                raise ValueError("insert error")

    def deal_data_by_ck(self):
        sql = 'select distinct fe_categories, fe_categorie_names from shopee_item where length(fe_categories) > 0'
        category_list = Clickhouse('clickhouse').execute(sql)
        while category_list:
            cat_ids, cat_names = category_list.pop(0)
            print('Current data/count: {}/{}'.format(cat_ids, len(category_list)))
            # log.info('Current data/count: {}/{}'.format(cat_ids, len(category_list)))
            cat_len = len(cat_ids)
            for index in range(cat_len):
                cat_info = deepcopy(self.mysql_key_map)
                cat_info['cid'] = cat_ids[index]
                cat_info['name'] = cat_names[index]
                cat_info['level'] = index + 1
                for level in range(index+1):
                    cat_info['lv{}cid'.format(level+1)] = cat_ids[level]
                    cat_info['lv{}name'.format(level+1)] = cat_names[level]
                # 子类目
                if index > 0:
                    cat_info['parent_cid'] = cat_ids[index-1]
                    cat_info['top_parent_cid'] = cat_ids[0]
                # 非底层类目
                if index < cat_len-1:
                    cat_info['is_parent'] = 1
                self.insert_queue.append(cat_info)
            if len(self.insert_queue) >= self.BATCH:
                if not self.insert_mysql():
                    raise ValueError("insert error")
        if not self.insert_mysql():
            raise ValueError("insert error")

    def insert_mysql(self):
        success_flag = True
        if not self.insert_queue:
            return success_flag
        sql = """insert ignore {} (
                    cid, parent_cid, top_parent_cid, name, lv1name, lv2name, lv3name, lv4name, lv1cid, lv2cid, lv3cid, lv4cid, 
                    is_parent, level
                ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update 
                parent_cid = if(values(parent_cid) <> 0, values(parent_cid), parent_cid), 
                top_parent_cid = if(values(top_parent_cid) <> 0, values(top_parent_cid), top_parent_cid), 
                name = if(values(name) <> '', values(name), name), 
                lv1name = if(values(lv1name) <> '', values(lv1name), lv1name), 
                lv2name = if(values(lv2name) <> '', values(lv2name), lv2name), 
                lv3name = if(values(lv3name) <> '', values(lv3name), lv3name), 
                lv4name = if(values(lv4name) <> '', values(lv4name), lv4name), 
                lv1cid = if(values(lv1cid) <> 0, values(lv1cid), lv1cid), 
                lv2cid = if(values(lv2cid) <> 0, values(lv2cid), lv2cid), 
                lv3cid = if(values(lv3cid) <> 0, values(lv3cid), lv3cid), 
                lv4cid = if(values(lv4cid) <> 0, values(lv4cid), lv4cid), 
                is_parent = if(values(is_parent) <> 0, values(is_parent), is_parent), 
                level = if(values(level) <> 0, values(level), level), 
                modified=now()
                """.format(self.db_table)
        insert_datas = []
        insert_key = [
                'cid', 'parent_cid', 'top_parent_cid', 'name', 'lv1name', 'lv2name', 'lv3name', 'lv4name', 'lv1cid', 'lv2cid', 'lv3cid', 'lv4cid', 
                'is_parent', 'level', 
        ]
        try:
            for i in self.insert_queue:
                insert_datas.append([i[key] for key in insert_key])
        except Exception as e:
            log.error('deal {} data failed: {}'.format(PROJECT, e))
            pass
        for _ in range(1, 3):
            try:
                print("Start insert sql data count=>{}".format(len(self.insert_queue)))
                # log.info("Start insert sql data count=>{}".format(len(self.insert_queue)))
                DB(Tool.get_mysql_config('shopee')).insert_many(sql, insert_datas)
                self.insert_queue = []
                print("Insert end")
                # log.info("Insert end")
                break
            except Exception as e:
                log.error('insert {} table failed: {}'.format(PROJECT, e))
                success_flag = False
                time.sleep(10)
                continue
        return success_flag


if __name__ == '__main__':
    hand = GetShopeeCatrgory()
    # curl请求处理
    # hand.deal_requests()
    # ck数据库数据处理
    hand.deal_data_by_ck()