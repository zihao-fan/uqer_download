# -*- coding: utf-8 -*-
import argparse
import os
import datetime
import json

today = datetime.datetime.now().strftime('%Y%m%d')
parser = argparse.ArgumentParser(description='Download and save data from uqer DataAPI')
parser.add_argument('--begin', help='下载起始日期 YYYYMMDD', type=str, default=today)
parser.add_argument('--end', help='下载结束日期 默认当日', type=str, default=today)
# freq choose from all, year, day, month
parser.add_argument('--freq', help='下载的频率，只下载对应频率的表格', type=str, default='')
parser.add_argument('--mode', help='下载的方式,单线程多天下载(period)or多线程逐天下载(day)', type=str, default='day')
args = parser.parse_args()

filename = 'api_dict.json'
api_dict = {}

with open(filename, 'r') as f:
    api_dict = json.load(f)

if len(args.freq) == 0:
    api_list = []
    for key, value in api_dict.items():
        api_list += value
else:
    api_list = api_dict[args.freq]

for api in api_list:
    command_str = ' '.join(['python', 'src/data_download.py', '--name', api, '--api', api, '--begin', args.begin, '--end', args.end, '--mode', args.mode])
    os.system(command_str)