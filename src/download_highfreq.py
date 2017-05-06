# -*- coding: utf-8 -*-
import pandas as pd
import os
import uqer
import uqer_utils
import threading
import Queue
import time
import argparse

from uqer_utils import root_path

today = uqer_utils.get_today()

parser = argparse.ArgumentParser(description='Download and save data from uqer DataAPI')
parser.add_argument('--id', help='下载股票的secID', type=str, default='000905.XSHE')
parser.add_argument('--begin', help='下载起始日期 YYYYMMDD', type=str, default='20070101')
parser.add_argument('--end', help='下载结束日期 默认当日', type=str, default=today)
parser.add_argument('--unit', help='下载的频率', type=int, default=1)

args = parser.parse_args()
data_dir = os.path.join(root_path, 'data', 'high_freq')

if __name__ == '__main__':
    client = uqer_utils.login()

    time_list = uqer_utils.get_time_list(args.begin, args.end)
    time_list = [t.replace('-', '') for t in time_list]
    
    frames = []
    for date in time_list:
        res = uqer.DataAPI.MktBarHistDateRangeGet(securityID=args.id,
            startDate=date,
            endDate=date,
            unit=args.unit,
            field=u"",
            pandas="1")
        frames.append(res.set_index('dataDate'))

    res = pd.concat(frames)

    outfile_name = args.id[:-5] + '_' + args.begin + '_' + args.end + '.data'
    save_path = os.path.join(data_dir, outfile_name)
    res.to_pickle(save_path)

    print 'Done. Save to', save_path