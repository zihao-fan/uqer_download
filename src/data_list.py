import uqer_utils

yesterday = uqer_utils.get_yesterday()
special_params_dict = {'MktAdjfAfMGet': {}, 'EquGet': {'equTypeCD':'A'}, 'EquRTRankGet': {}, 'SecTypeGet': {}, 'EquManagersInfoGet': {},
                        'SecTypeRegionRelGet': {}, 'PartyIDGet': {}, 'IndustryGet': {}, 'EquIndustryGet': {}, 'EquPartyNatureGet': {},
                        'SecIDGet': {}, 'EquSHHKConsGet': {}, 'SecTypeRegionGet': {}, 'SecTypeRelGet': {}, 
                        'MktCBOMOGet': {'omoType':"1,2,3,4,5", 'beginDate':yesterday, 'endDate':yesterday}, 'EquShareFloatGet':{},
                        'MktFutOiRatioGet':{'beginDate':yesterday, 'endDate':yesterday}, 'equSZHKConsGet':{'exchangeCD':'SZSC'}, 'equSZHKQuotaGet':{},
                        'equSZHKTDTenGet':{}, 'BondConvPriceChgGet':{}, 'RepoGet':{}, 'TkgThemesGet':{}, 'NewsInfoByInsertTimeGet':{},
                        'equSHHKTDTenGet':{}, 'NewsInfoByTimeGet':{}, 'NewsPublishSiteGet':{}, 'equSHHKstatsTDGet':{},
                        'IdxGet':{}, 'SocialDataXQByDateGet':{}, 'NewsInfoByTimeAndSiteGet':{},
                        'equSZHKstatsTDGet':{}}
publish_date_list = ['FdmtBSInduGet', 'FdmtISInduGet', 'FdmtIndiGrowthPitGet', 'FdmtIndiPSPitGet', 'FdmtCFBankGet', 'FdmtISSecuGet', 
                    'FdmtCFInsuGet', 'FdmtBSInsuGet', 'FdmtCFInduGet', 'FdmtIndiRtnPitGet', 'FdmtIndiTrnovrPitGet', 'FdmtISGet',
                    'FdmtCFSecuGet', 'FdmtBSBankGet', 'FdmtDerPitGet', 'FdmtBSGet', 'FdmtCFGet', 'FdmtBSSecuGet',
                    'FdmtISBankGet', 'FdmtISInsuGet', 'FdmtCFSecuGet', 'FdmtEfGet', 'FdmtEeGet']
trade_date_list = ['MktLimitGet', 'MktMFutdGet', 'MktStockFactorsOneDayProGet', 'equSHHKQuotaGet', 'equSZHKForexGet', 
                   'MktOptUlHvGet', 'equSZHKForexGet', 'MktIdxFactorOneDayGet']
by_day_list = ['NewsInfoByInsertTimeGet', 'NewsInfoByTimeGet', 'SocialDataXQByDateGet', 'NewsInfoByTimeAndSiteGet'] + trade_date_list

skip_list = ['FutuGet', 'ReportContentGet', 'SocialDataXQByTickerGet', 'BondIssueGet', 'NewsInfoGet', 'BondSizeChgGet',
'BondOptionGet', 'MktOptVolatilityGet', 'FundGet', 'OptGet', 'NewsByTickersGet', 'ReportContentByIDGet', 'BondGet', 'TkgThemeTickerRelGet',
'mIdxCloseWeightGet', 'ReportByTickerGet', 'TkgThemeNewsRelGet', 'BondCouponGet', 'HKFdmtBSGet', 'NewsBodyGet', 'HKFdmtCFGet', 'BondGuarGet', 'HKEquGet',
'FundManagerGet', 'FundLeverageInfoGet', 'OptVarGet', 'HKEquCAGet', 'TickersByNewsGet', 'IdxConsGet', 'IdxCloseWeightGet', 'NewsByCompanyGet', 'FutuConvfGet',
'CompanyByNewsGet', 'MktOptUlHvGet', 'SocialDataGubaGet', 'MktIdxFactorOneDayGet', 'BondAiHSGet', 'TkgThemeHotGet']