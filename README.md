# uqer_download

## 使用说明

仅支持Python2  
用来通过uqer的DataAPI下载文件到本地并存档在./data目录下。  
使用DataAPI需要登录uqer账号，账号的说明文件存在本项目根目录下并命名为 'account.txt'  

目前的下载逻辑为，指定需要的表格，股票secID，起始日期，中止日期，下载并保存。


    python --name 表格名称 --api API函数名 --begin YYYYMMDD --end YYYYMMDD --threads 线程个数 --params 额外参数
    例如：python data_download.py --name MktEqudAdjGet --api MktEqudAdjGet --params '{"isOpen" : 1}'
    
