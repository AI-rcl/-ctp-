from event.event import *
from event.event_engine import EventEngine,Event
from ctpapi import CtpMdApi,CtpTdApi
from cta import CtaEngine
from config import *
from ui import *


class MainEngine(object):

    def __init__(self) -> None:
        
        self.ee = EventEngine()
        self.ce = CtaEngine(self,self.ee)
        self.md = CtpMdApi(self.ee)
        #self.td = CtpTdApi(self.ee)
        self.ee.start() 

        self.userID = user          # 账号
        self.password = password       # 密码
        self.brokerID = broker_id        # 经纪商代码
        self.MdIp = fronts["电信2"]['md']       # 行情服务器地址
        self.TdIp = fronts["电信2"]['td']         # 交易服务器地址
        self.authCode = authcode        # 授权码
        self.appID = appid          # 软件代号
        self.userProductInfo = '' # 产品信息
        
        self.mv = MainWindow(self,self.ee)
        
        self.mv.showMaximized()
    
    def login(self):
        self.md.connect(self.userID, self.password, self.brokerID, self.MdIp)
        #self.td.connect(self.userID, self.password, self.brokerID, self.TdIp, self.appID, self.authCode, self.userProductInfo)
    
    def subscribe(self, req):
        '''订阅行情'''
        self.md.subscribe(req)
    
    def unsubscribe(self,req):
        '''退订行情'''
        self.md.unsubscribe(req)
        

if __name__ == "__main__":
    app = QApplication([])
    try:
        import qdarkstyle
        #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())   # 黑色主题
        app.setFont(QFont("Microsoft YaHei", 11))               # 微软雅黑字体
    except:
        pass
    
    main = MainEngine()
    main.login()
    #main.subscribe('rb2405')
    app.exec()