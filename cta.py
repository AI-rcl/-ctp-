from event.event_engine import EventEngine,Event
from event.event import *
import datetime
import traceback

class CtaEngine(object):

    def __init__(self,main_engine, event_engine) -> None:
        self.me = main_engine
        self.ee = event_engine
        self.ee.register(EVENT_TICK,self.process_tick_event)
    
    def process_tick_event(self,event):

        tick = event.dict_['data']
        #print(tick.symbol,tick.bidPrice1,tick.bidVolume1,tick.askPrice1,tick.askVolume1)
         # 收到tick行情后，先处理本地停止单（检查是否要立即发出）
        # self.processStopOrder(tick)
        
        # # 推送tick到对应的策略实例进行处理
        # if tick.vtSymbol in self.tickStrategyDict:
        #     # tick时间可能出现异常数据，使用try...except实现捕捉和过滤
        #     try:
        #         # 添加datetime字段
        #         if not tick.datetime:
        #             tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
        #     except ValueError:
        #         self.writeCtaLog(traceback.format_exc())
        #         return
                
        #     # 逐个推送到策略实例中
        #     l = self.tickStrategyDict[tick.vtSymbol]
        #     for strategy in l:
        #         self.callStrategyFunc(strategy, strategy.onTick, tick)