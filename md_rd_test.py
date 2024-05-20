from vnpy_ctptest.api import MdApi,TdApi
from api.thostmduserapi import CThostFtdcMdApi,CThostFtdcMdSpi
from event.event_engine import *
from event.event import *
from data_type import *
from objects import *

from time import sleep
from datetime import datetime, time
import random
import os
from copy import copy
from config import *

class CtpMdApi(MdApi):
    """
    Demo中的行情API封装
    封装后所有数据自动推送到事件驱动引擎中，由其负责推送到各个监听该事件的回调函数上

    对用户暴露的主动函数包括:
    连接connect
    登陆 login
    订阅合约 subscribe
    """
    def __init__(self, eventEngine):
        """
        API对象的初始化函数
        """
        super(CtpMdApi, self).__init__()

        self.__eventEngine = eventEngine
        
        self.reqID = 0              # 操作请求编号
        
        self.connectionStatus = False       # 连接状态
        self.loginStatus = False            # 登录状态
        
        self.subscribedSymbols = []      # 已订阅合约代码       
        self.TradingDay = ''
        
        self.userID =   user      # 账号
        self.password = password       # 密码
        self.brokerID = broker_id        # 经纪商代码
        self.address = fronts['电信2']['md']         # 服务器地址
        self.gatewayName = 'CTPTEST'    # 网关名称
        
    def put_log_event(self, log):  # log事件注册
        event = Event(type_=EVENT_LOG)
        event.dict_['log'] = log
        self.__eventEngine.put(event)
        
    def put_alarm_event(self, alarm):  # log事件注册
        event = Event(type_=EVENT_ALARM)
        event.dict_['data'] = alarm
        self.__eventEngine.put(event)
        
    def onFrontConnected(self):
        """服务器连接"""
        self.connectionStatus = True
        
        log = u'行情服务器连接成功'
        self.put_log_event(log)
        print('行情服务器连接成功')

        self.login()
    #----------------------------------------------------------------------  
    def onFrontDisconnected(self, n):
        """服务器断开"""
        self.connectionStatus = False
        self.loginStatus = False

        log = u'行情服务器连接断开'
        self.put_log_event(log)
        
        now = datetime.now().time()
        if time(8, 48) < now < time(15, 30) or time(20, 48) < now <= time(23, 59) or time(0, 0) < now < time(2, 31):
            alarm = '行情服务器断开连接'
            self.put_alarm_event(alarm)
    #----------------------------------------------------------------------  
    def login(self):
        """登录"""
        # 如果填入了用户名密码等，则登录
        if self.userID and self.password and self.brokerID:
            req = {}
            req['UserID'] = self.userID
            req['Password'] = self.password
            req['BrokerID'] = self.brokerID
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)    

    #----------------------------------------------------------------------
    def close(self):
        """关闭"""
        self.exit()
        
    def connect(self, userID, password, brokerID, address):
        """初始化连接"""
        self.userID = userID                # 账号
        self.password = password            # 密码
        self.brokerID = brokerID            # 经纪商代码
        self.address = address              # 服务器地址
        
        # 如果尚未建立服务器连接，则进行连接
        if not self.connectionStatus:
            # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
            path = os.getcwd() + '/temp/'
            if not os.path.exists(path):
                os.makedirs(path)
            self.createFtdcMdApi(path)
            
            # 注册服务器地址
            self.registerFront(self.address)
            
            
            # 初始化连接，成功会调用onFrontConnected
            self.init()
            
        # 若已经连接但尚未登录，则进行登录
        else:
            if not self.loginStatus:
                self.login()
                
    def onRtnDepthMarketData(self, data):
        """行情推送"""
        if not data['Volume']:
            return
        
        # 创建对象
        tick = CtaTickData()
        
        tick.symbol = data['InstrumentID']
        tick.exchange = data['ExchangeID']   #exchangeMapReverse.get(data['ExchangeID'], u'未知')
        tick.vtSymbol = tick.symbol #'.'.join([tick.symbol, EXCHANGE_UNKNOWN]) # 只用到ctp一个接口，这里没有必要区分
        
        tick.lastPrice = data['LastPrice']
        tick.volume = data['Volume']
        tick.openInterest = data['OpenInterest']
        

        tick.time = '.'.join([data['UpdateTime'], str(int(data['UpdateMillisec']/100))])
        # 不带毫秒的时间，方便转换datetime
        tick.time2 = data['UpdateTime'] 
        # 把交易日也保存下来，转换datetime用  
        tick.tradedate = self.TradingDay
        # print('tick.tradedate:%s'%tick.tradedate)
        
        # 这里由于交易所夜盘时段的交易日数据有误，所以选择本地获取
        tick.date = datetime.now().strftime('%Y%m%d')   
        
        tick.openPrice = data['OpenPrice']
        tick.highPrice = data['HighestPrice']
        tick.lowPrice = data['LowestPrice']
        tick.preClosePrice = data['PreClosePrice']
        
        tick.upperLimit = data['UpperLimitPrice']
        tick.lowerLimit = data['LowerLimitPrice']
        
        # CTP只有一档行情
        # 无报价时用涨跌停板价替换,如果没有推送涨跌停价会出错，可以自行用一个很大的数字替代，或者就用推送的巨大数字
        # if data['BidPrice1'] > tick.upperLimit:
        #     tick.bidPrice1 = tick.lowerLimit
        # else:
        #     tick.bidPrice1 = data['BidPrice1']
        # if data['AskPrice1'] > tick.upperLimit:
        #     tick.askPrice1 = tick.upperLimit
        # else:
        #     tick.askPrice1 = data['AskPrice1']
        tick.askPrice1 = data['AskPrice1']
        tick.bidPrice1 = data['BidPrice1']

        tick.bidVolume1 = data['BidVolume1']
        tick.askVolume1 = data['AskVolume1']
        
        event1 = Event(type_=(EVENT_TICK + data['InstrumentID']))
        event1.dict_['data'] = tick
        self.__eventEngine.put(event1)

        event2 = Event(type_=(EVENT_TICK))
        event2.dict_['data'] = tick
        #print(tick.datetime,tick.symbol,tick.askPrice1,tick.bidPrice1)
        self.__eventEngine.put(event2)
        
    def subscribe(self, symbol):
        """订阅合约"""
        # 这里的设计是，如果尚未登录就调用了订阅方法
        # 则先保存订阅请求，登录完成后会自动订阅
        if symbol not in self.subscribedSymbols:
            if self.loginStatus:
                self.subscribeMarketData(str(symbol))
            self.subscribedSymbols.append(symbol)
            event = Event(type_=EVENT_SUB)
            event.dict_['symbol'] = symbol
            self.__eventEngine.put(event)
        print('订阅成功')
        
    #----------------------------------------------------------------------
    def unsubscribe(self, symbol):
        """退订合约"""
        self.unSubscribeMarketData(str(symbol))
        
    #----------------------------------------------------------------------   
    def onRspError(self, error, n, last):
        """错误回报"""
        log = error['ErrorMsg']
        self.put_log_event(log)
        
    #----------------------------------------------------------------------
    def onRspUserLogin(self, data, error, n, last):
        """登陆回报"""
        # 如果登录成功，推送日志信息
        if not error or 0 == error['ErrorID']:
            self.loginStatus = True
            
            log = u'行情服务器登录完成'
            self.put_log_event(log)
            print(error)
            print(n)
            print(last)
            # 重新订阅之前订阅的合约
            for symbol in self.subscribedSymbols:
                self.subscribe(symbol)
                
        # 否则，推送错误信息
        else:
            log = error['ErrorMsg']
            self.put_log_event(log)

    #---------------------------------------------------------------------- 
    def onRspUserLogout(self, data, error, n, last):
        """登出回报"""
        # 如果登出成功，推送日志信息
        if not error or 0 == error['ErrorID']:
            self.loginStatus = False
            self.gateway.mdConnected = False
            
            log = u'行情服务器登出完成'
            self.put_log_event(log)
                
        # 否则，推送错误信息
        else:
            log = error['ErrorMsg'].decode('gbk')
            self.put_log_event(log)
        
    #----------------------------------------------------------------------  
    def onRspSubMarketData(self, data, error, n, last):
        """订阅合约回报"""
        # 通常不在乎订阅错误，选择忽略
        
    
        
    #----------------------------------------------------------------------  
    def onRspUnSubMarketData(self, data, error, n, last):
        """退订合约回报"""
        # 同上
        pass  

class Strategy:
    
    def __init__(self,eventEngine) -> None:
        self.ee = eventEngine
        self.ee.register(EVENT_TICK,self.get_tick)
    
    def get_tick(self,event):
        tick = event.dict_['data']

        print(f"收到tick:{tick.symbol},{tick.askPrice1},{tick.bidPrice1}")

if __name__ == "__main__":
    ee = EventEngine()

    mdapi = CtpMdApi(ee) 
    rb = Strategy(ee)
    ee.start()
    mdapi.connect(user,password,broker_id,fronts['电信1']['md'])
    mdapi.subscribe('rb2405')
    #mdapi.subscribe('eg2405')
    
    
    
