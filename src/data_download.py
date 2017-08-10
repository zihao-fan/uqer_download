# -*- coding: utf-8 -*-
import pandas as pd
import os
import uqer
import uqer_utils
import threading
import Queue
import time
import argparse
import json
import datetime
from dateutil.parser import parse

from uqer import DataAPI
from uqer_utils import root_path
from data_list import special_params_dict, publish_date_list, trade_date_list, skip_list, by_day_list

today = uqer_utils.get_today()
yesterday = uqer_utils.get_yesterday()

parser = argparse.ArgumentParser(description='Download and save data from uqer DataAPI')
parser.add_argument('--begin', help='下载起始日期 YYYYMMDD', type=str, default=yesterday)
parser.add_argument('--end', help='下载结束日期 默认当日', type=str, default=yesterday)
parser.add_argument('--threads', help='程序下载使用进程数', type=int, default=1)
parser.add_argument('--params', help='API所需要的其他参数', type=str, default='')
parser.add_argument('--mode', help='下载的方式,单线程多天下载(period)or多线程逐天下载(day)', type=str, default='day')

args = parser.parse_args()

fail_set = set()
current_name = ''

class ConsumerThread(threading.Thread):
    def __init__(self, queue, api, params, path, name=None):
        super(ConsumerThread, self).__init__()
        self.name = name
        self.q = queue
        self.api = api 
        self.params = params
        self.path = path
        return

    def run(self):
        while not self.q.empty():
                date = self.q.get()
                try:
                    current_dict = self.params.copy()
                    if current_name in special_params_dict :
                        current_dict.update(special_params_dict[current_name])
                        if 'beginDate' in current_dict:
                            current_dict['beginDate'] = date
                            current_dict['endDate'] = date
                        if current_name == 'EquShareFloatGet':
                            current_dict['beginfloatDate'] = date
                            current_dict['endfloatDate'] = date
                        if current_name == 'MktFutOiRatioGet':
                            secList =  DataAPI.SysCodeGet(codeTypeID=u"60003",valueCD=u"",field=u"",pandas="1").valueCD.tolist()
                            current_dict['contractObject'] = secList
                        if current_name == 'NewsInfoByInsertTimeGet':
                            current_dict['newsInsertDate'] = date
                        if current_name == 'NewsInfoByTimeGet' or current_name == 'NewsInfoByTimeAndSiteGet':
                            current_dict['newsPublishDate'] = date
                        if current_name == 'SocialDataXQByDateGet':
                            current_dict['statisticsDate'] = date
                    elif current_name in publish_date_list:
                        current_dict['publishDateBegin'] = date
                        current_dict['publishDateEnd'] = date
                    elif current_name in trade_date_list:
                        current_dict['tradeDate'] = date
                    else:
                        current_dict['beginDate'] = date
                        current_dict['endDate'] = date
                    res = self.api(**current_dict)
                    store_path = os.path.join(self.path, date+'.h5')
                    res.to_hdf(store_path, 'df')
                    print '[Success] Getting ' + str(date) + '\n'
                except Exception as e:
                    # self.q.put(date)
                    fail_set.add(current_name)
                    print e
                    print '[Failed]' + str(date) + '\n'
        return

def get_date_str(text):
    date = parse(text)
    return date.strftime('%Y-%m-%d')

def get_date_filename(begin_date, end_date):
    if begin_date != end_date:
        date_name = get_date_str(begin_date) + '+' + get_date_str(end_date)
    else:
        date_name = get_date_str(begin_date)
    return date_name

class DataDownloader(object):
    
    def __init__(self, chart_name, begin_date, end_date, params, mode):
        print '[Chart]', chart_name, 'downloading.'
        self.chart_name = chart_name
        self.api = getattr(DataAPI, chart_name) # function pointer already
        self.params = {}
        self.mode = mode
        try:
            self.params = json.loads(params)
            print 'Using auxiliary params.'
        except:
            print 'No auxiliary params.'
        print 'Self params', self.params
        
        # data dir
        data_dir = os.path.join(root_path, 'data')
        if not os.path.exists(data_dir):
            print 'Creating directory:', data_dir
            os.makedirs(data_dir)

        # chart dir
        self.data_path = os.path.join(data_dir, chart_name)
        if not os.path.exists(self.data_path):
            print 'Creating directory:', self.data_path
            os.makedirs(self.data_path)

        if self.mode == 'day':
            print 'Using multi-thread mode. Download by a single day.'
            self.queue = Queue.Queue()
            self.date_list = uqer_utils.get_time_list(begin_date, end_date)
            print 'date list', self.date_list
            [self.queue.put(date) for date in self.date_list]
            self.worker_list = [ConsumerThread(self.queue, self.api, 
                                self.params, self.data_path, 
                                name='thread'+str(i+1)) for i in range(args.threads)]
        elif self.mode == 'period':
            print 'Using single thread mode. Download by many days.'
            self.begin_date = begin_date
            self.end_date = end_date

    def single_thread_download(self):
        try:
            current_dict = self.params.copy()
            if current_name in special_params_dict:
                current_dict.update(special_params_dict[current_name])
                if 'beginDate' in current_dict:
                    current_dict['beginDate'] = self.begin_date
                    current_dict['endDate'] = self.end_date
                if current_name == 'EquShareFloatGet':
                    current_dict['beginfloatDate'] = self.begin_date
                    current_dict['endfloatDate'] = self.end_date
                if current_name == 'MktFutOiRatioGet':
                    secList =  DataAPI.SysCodeGet(codeTypeID=u"60003",valueCD=u"",field=u"",pandas="1").valueCD.tolist()
                    current_dict['contractObject'] = secList
            elif current_name in publish_date_list:
                current_dict['publishDateBegin'] = self.begin_date
                current_dict['publishDateEnd'] = self.end_date
            else:
                current_dict['beginDate'] = self.begin_date
                current_dict['endDate'] = self.end_date
            res = self.api(**current_dict)
            date_name = get_date_filename(self.begin_date, self.end_date)
            store_path = os.path.join(self.data_path, date_name+'.h5')
            res.to_hdf(store_path, 'df')
            print '[Success] Getting ' + str(date_name) + '\n'
        except Exception as e:
            fail_set.add(current_name)
            print e
            print '[Failed]' + str(self.begin_date) + ' ' + str(self.end_date) + '\n'

    def download(self):
        start_time = time.time()
        if self.mode == 'day':
            [w.start() for w in self.worker_list]
            [w.join() for w in self.worker_list]
        if self.mode == 'period':
            self.single_thread_download()
        print 'Done downloading in %s minutes' % str((time.time() - start_time) / 60)

if __name__ == '__main__':
    client = uqer_utils.login()

    # could alter here 
    with open('../set_v1.json', 'r') as f:
        set_v1 = set(json.load(f))
    with open('../set_v3.json', 'r') as f:
        set_v3 = set(json.load(f))

    # download_list = list(set_v3) # all forms
    download_list = list(set_v3 - set_v1) # new forms
    # download_list = [] # self defining forms

    for item in download_list:
        current_name = item
        if current_name in skip_list:
            continue
        if current_name in by_day_list:
            downloader = DataDownloader(current_name, args.begin, args.end, args.params, 'day')
        else:
            downloader = DataDownloader(current_name, args.begin, args.end, args.params, args.mode)
        downloader.download()

    fail_list = list(fail_set)
    date_name = get_date_filename(args.begin, args.end)
    log_path = os.path.join(root_path, 'logs', date_name+'.log')
    with open(log_path, 'w') as f:
        json.dump(fail_list, f)
    print 'Log info dumped to', log_path