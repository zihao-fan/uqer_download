# -*- coding: utf-8 -*-
import datetime
from dateutil.parser import parse
import pandas as pd 
import os

import uqer
from uqer import DataAPI

current_path = os.path.realpath(__file__)
root_path = '/'.join(current_path.split('/')[:-2])

def login():
    account_file_path = os.path.join(root_path, 'account.txt')
    client = uqer.Client(account_file=account_file_path)
    return client

def get_today():
    '''
    return a str 'YYYYMMDD'
    '''
    return datetime.datetime.now().strftime('%Y%m%d')

def get_data_filename_from_path(path, max_num=None):
    data_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.data')]
    if max_num is not None:
        data_files = data_files[0:min(max_num, len(csv_files))]
    return data_files

def ticker2secID(ticker):
    """
    给定股票代码转化为股票内部编码
    Args:
        tickers (list): 需要转化的股票代码列表
    Returns:
        list: 转化为内部编码的股票编码列表

    Examples:
        >> tickers = ['600000','000001']
        >> secIDs = ticker2secID(tickers)
    """
    universe = DataAPI.EquGet(equTypeCD=u"A", listStatusCD="L,S,DE,UN", 
                            field=u"ticker,secID", pandas="1") # 获取所有的A股（包括已退市）
    universe = dict(universe.set_index('ticker')['secID'])
    if isinstance(ticker, list):
        res = []
        for i in ticker:
            if i in universe:
                res.append(universe[i])
            else:
                print i, ' 在universe中不存在，没有找到对应的secID！'
        return res
    else:
        raise ValueError('ticker should be list！')

def secID2ticker(secID):
    """
    给定股票内部编码转化为股票代码
    Args:
        secIDs (list): 需要转化的股票编码列表
    Returns:
        list: 转化为股票代码的列表

    Examples:
        >> secIDs = set_universe('HS300')
        >> tickers = secID2ticker(secIDs)
    """
    universe = DataAPI.EquGet(equTypeCD=u"A", listStatusCD="L,S,DE,UN", 
                              field=u"ticker,secID", pandas="1") # 获取所有的A股（包括已退市）
    universe = dict(universe.set_index('secID')['ticker'])
    if isinstance(secID, list):
        res = []
        for i in secID:
            if i in universe:
                res.append(universe[i])
            else:
                print i, ' 在universe中不存在，没有找到对应的secID！'
        return res
    else:
        raise ValueError('secID should be list！')

def st_remove(source_universe, st_date=None):
    """
    给定股票列表,去除其中在某日被标为ST的股票
    Args:
        source_universe (list of str): 需要进行筛选的股票列表
        st_date (datetime): 进行筛选的日期,默认为调用当天
    Returns:
        list: 去掉ST股票之后的股票列表

    Examples:
        >> universe = set_universe('A')
        >> universe_without_st = st_remove(universe)
    """
    st_date = st_date if st_date is not None else datetime.datetime.now().strftime('%Y%m%d')
    df_ST = DataAPI.SecSTGet(secID=source_universe, beginDate=st_date, endDate=st_date, field=['secID'])
    return [s for s in source_universe if s not in list(df_ST['secID'])]

def get_time_list(start_date, end_date):
    """
    给定开始日期和结束日期，返回其中的所有日期
    Args:
        start_date (str or datetime): 开始日期，常见日期格式支持
        end_date (str ot datetime): 结束日期，常见日期格式支持
    Returns:
        list: str,‘%Y-%m-%d’格式的日期列表

    Examples:
        >> time_list = get_time_list('20150101','20160101')
    """
    start_date = parse(start_date)
    end_date = parse(end_date)
    time_list = []
    while (start_date < end_date): 
        time_list.append((start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
        start_date = start_date + datetime.timedelta(days=1)
    return time_list

if __name__ == '__main__':
    pass
    # today = datetime.datetime.now().strftime('%Y%m%d')
    # print 'today', today, type(today)

    # tickers = ['600000','000001']
    # res = secIDs = ticker2secID(tickers)
    # print 'ticker2secID', res

    # universe = DataAPI.EquGet(equTypeCD=u"A", listStatusCD="L,S,DE,UN", 
    #                         field=u"ticker,secID", pandas="1")
    # universe_secID = list(universe['secID'])
    # universe_without_st = st_remove(universe_secID)
    # print 'universe_without_st', universe_without_st

    # time_list = get_time_list('20150101','20160101')
    # print 'time_list', time_list