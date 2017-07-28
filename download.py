# -*- coding: utf-8 -*-
import argparse
import os
import datetime

today = datetime.datetime.now().strftime('%Y%m%d')
parser = argparse.ArgumentParser(description='Download and save data from uqer DataAPI')
parser.add_argument('--begin', help='下载起始日期 YYYYMMDD', type=str, default=today)
parser.add_argument('--end', help='下载结束日期 默认当日', type=str, default=today)
args = parser.parse_args()

api_list = ['MktIndustryFlowOrderGet', 'MktEqudAdjGet', 'MktNeeqEqudGet', 'MktRankListStocksGet',
            'MktAdjfGet', 'MktAdjfAfMGet', 'MktEquFlowGet', 'SecHaltGet', 'MktEqudAdjAfGet',
            'MktLimitGet', 'MktBlockdGet', 'MktIpoConTraddaysGet', 'MktHKEqudGet',
            'MktAHCompdGet', 'MktRankListSalesGet', 'MktVolAdjfGet', 'MktSubnewEqudGet']

for api in api_list:
    command_str = ' '.join(['python', 'src/data_download.py', '--name', api, '--api', api, '--begin', args.begin, '--end', args.end])
    os.system(command_str)