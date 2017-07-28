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

from uqer import DataAPI
from uqer_utils import root_path

today = uqer_utils.get_today()

parser = argparse.ArgumentParser(description='Download and save data from uqer DataAPI')
parser.add_argument('--name', help='输入你要下载的表格名称，程序会根据该名称创建目录。', type=str, required=True)
parser.add_argument('--api', help='表格对应的API名称，字符串形式', type=str, required=True)
parser.add_argument('--begin', help='下载起始日期 YYYYMMDD', type=str, default=today)
parser.add_argument('--end', help='下载结束日期 默认当日', type=str, default=today)
parser.add_argument('--threads', help='程序下载使用进程数', type=int, default=1)
parser.add_argument('--params', help='API所需要的其他参数', type=str, default='')

args = parser.parse_args()

no_params_list = ['MktAdjfAfMGet']
trade_date_list = ['MktLimitGet']

class ConsumerThread(threading.Thread):
    def __init__(self, queue, api, params, path, name=None):
        super(ConsumerThread, self).__init__()
        self.name = name
        self.q = queue
        self.api = api 
        self.params = params
        self.path = path
        self.universe = universe
        return

    def run(self):
        while not self.q.empty():
                date = self.q.get()
                try:
                    current_dict = self.params.copy()
                    if args.name in no_params_list :
                        print 'Not passing any params.'
                    elif args.name in trade_date_list:
                        current_dict['tradeDate'] = date
                    else:
                        current_dict['beginDate'] = date
                        current_dict['endDate'] = date
                    res = self.api(**current_dict)
                    store_path = os.path.join(self.path, date+'.pkl')
                    res.to_pickle(store_path)
                    print '[Success] Getting ' + str(date)
                except Exception as e:
                    # self.q.put(date)
                    print e
                    print '[Failed]' + str(date)
        return

class DataDownloader(object):
    
    def __init__(self, chart_name, api, begin_date, end_date, params):
        print '[Chart]', chart_name, 'downloading.'
        self.chart_name = chart_name
        self.api = getattr(DataAPI, api)
        self.params = {}
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

        self.queue = Queue.Queue()
        self.date_list = uqer_utils.get_time_list(begin_date, end_date)
        print 'date list', self.date_list
        [self.queue.put(date) for date in self.date_list]
        self.worker_list = [ConsumerThread(self.queue, self.api, 
                            self.params, self.data_path, 
                            name='thread'+str(i+1)) for i in range(args.threads)]

    def download(self):
        start_time = time.time()
        [w.start() for w in self.worker_list]
        [w.join() for w in self.worker_list]
        # check if all done
        print 'Done downloading in %s minutes' % str((time.time() - start_time) / 60)
        all_file_downloaded = uqer_utils.get_data_filename_from_path(self.data_path)
        downloaded_set = set([f.split('.')[0] for f in all_file_downloaded])
        print 'downloaded_set', downloaded_set
        date_set = set(self.date_list)
        print 'date_set', date_set
        if date_set == downloaded_set:
            print '[Chart]', self.chart_name, 'All downloaded.'
        else:
            file_left = date_set - downloaded_set
            print '%d files missing' % len(file_left)
            print ''
            return list(file_left)
        print ''

if __name__ == '__main__':
    client = uqer_utils.login()
    universe = DataAPI.EquGet(equTypeCD=u"A", listStatusCD="L,S,DE,UN", 
                             field=u"ticker,secID", pandas="1")
    universe_secID = list(universe['secID'])

    # for debug
    stock_num = 10
    universe_secID = universe_secID[0:stock_num]

    downloader = DataDownloader(args.name, args.api, args.begin, args.end, args.params)
    downloader.download()