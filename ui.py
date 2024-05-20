from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from event.event_engine import Event,EventEngine
from event.event import *
import os
from datetime import date,datetime
import logging 

Qt.DockWidgetArea.RightDockWidgetArea

class MainWindow(QMainWindow):
    """主窗口"""
    # signal = pyqtSignal(type(Event()))
    #----------------------------------------------------------------------
    def __init__(self,main_engine,even_engine):
        """Constructor"""
        super(MainWindow, self).__init__()
        self.name = "main_window"
        self.widgetDict = {}    # 用来保存子窗口的字典
        self.me = main_engine 
        self.ee = even_engine

        self.initUi()
    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle("CTP DEMO——基于vnpy的ctp接口")
        self.setWindowIcon(QIcon('resource/fs.ico'))
        
        widgetMaket, Market = self.createDock(MarketMonitor, '行情', Qt.RightDockWidgetArea, engine=None, floatable=True)
        widgetTrading, Trading = self.createDock(TradingMonitor,'交易',Qt.LeftDockWidgetArea, engine=self.me,floatable=True)

        Market.raise_()
        Market.setMinimumWidth(260)
        Market.setFixedSize(1400,200)
        Market.setAllowedAreas(Qt.NoDockWidgetArea)

        Trading.raise_()
        Trading.setMinimumSize(300,500)
        Trading.setAllowedAreas(Qt.NoDockWidgetArea)
        
        aboutAction = QAction(u'关于', self)
        aboutAction.triggered.connect(self.openAbout)    
        
        rmAction = QAction(u'风险管理', self)
        # rmAction.triggered.connect(self.openRM)   
        
        menubar = self.menuBar()
        sysMenu = menubar.addMenu(u'系统')
        sysMenu.addAction(rmAction)
        helpMenu = menubar.addMenu(u'帮助')
        helpMenu.addAction(aboutAction)

    def openAbout(self):
        """打开关于"""
        try:
            self.widgetDict['aboutW'].show()
        except KeyError:
            self.widgetDict['aboutW'] = AboutWidget(self)
            self.widgetDict['aboutW'].show()

    def createDock(self, widgetClass, widgetName, widgetArea, engine=None, floatable=False):
            """创建停靠组件"""
            widget = widgetClass(self.ee, engine) if engine else widgetClass(self.ee) 
    
            dock = QDockWidget(widgetName)
            dock.setWidget(widget)
            dock.setObjectName(widgetName)
            if floatable:
                dock.setFeatures(dock.DockWidgetFloatable|dock.DockWidgetMovable|dock.DockWidgetClosable)
                #dock.setFeatures(dock.DockWidgetMovable|dock.DockWidgetClosable)
            else:
                dock.setFeatures(dock.DockWidgetMovable)
            self.addDockWidget(widgetArea, dock) 
            return widget, dock
    
class AboutWidget(QDialog):
    """显示关于信息"""

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(AboutWidget, self).__init__(parent)

        self.initUi()

    #----------------------------------------------------------------------
    def initUi(self):
        """"""
        self.setWindowTitle(u'关于刀削面')

        text = u"""
            Developed by vvipi.

            感谢VNPY！
            
            感谢PYCTP！

            感谢何先生的封装教程！
            
            本交易助手是为刀削面定制的自动交易终端
            交易策略采用土鳖交易法则
            
            八月，是期货投机最危险的月份，同样危险的月份还有：
            二月、十月、七月、三月、六月、一月、十二月、十一月、五月、九月、四月。
            
            刀削面加油！
            
            2017.8
            
            """

        label = QLabel()
        label.setText(text)
        label.setMinimumWidth(500)

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)    

class MarketMonitor(QTableWidget):

    signal = pyqtSignal(type(Event()))
    #----------------------------------------------------------------------
    def __init__(self,eventEngine,parent=None):
        """Constructor"""
        super(MarketMonitor, self).__init__(parent)
        self.__eventEngine = eventEngine
        self.setWindowTitle('行情')
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['时间','合约', '最新价','买一量','买一价','卖一价','卖一量'])
        #self.verticalHeader().setVisible(False)                 # 关闭左边的垂直表头
        self.setEditTriggers(QTableWidget.NoEditTriggers) # 设为不可编辑状态
        self.sub_symbols = []
        # self.setColumnWidth(0, 80)
        # self.setColumnWidth(1, 80)
        # Qt图形组件的GUI更新必须使用Signal/Slot机制，否则有可能导致程序崩溃
        # 因此这里先将图形更新函数作为Slot，和信号连接起来
        # 然后将信号的触发函数注册到事件驱动引擎中
        self.signal.connect(self.updateLog)
        self.__eventEngine.register(EVENT_TICK, self.signal.emit)
        self.insertRow(0)
    #     #保存日志到文件
    #     path = os.getcwd()+'/vnpy_engine_test/pyqt5/log/eventLog{date}'.format(date=date.today())
    #     logging.basicConfig(filename=path, level=logging.INFO)
    # #----------------------------------------------------------------------
    def updateLog(self, event):
        """更新日志"""
        # 获取当前时间和日志内容
        t = datetime.now()
        t = t.strftime('%H:%M:%S')
        tick = event.dict_['data']


        # 创建单元格
        #['时间','合约', '最新价','买一量','买一价','卖一价','卖一量']
        cell_time = QTableWidgetItem(t)
        cell_symbol = QTableWidgetItem(tick.symbol)
        cell_last_price = QTableWidgetItem(str(tick.lastPrice))
        cell_bid_volume = QTableWidgetItem(str(tick.bidVolume1))
        cell_bid_price = QTableWidgetItem(str(tick.bidPrice1))
        cell_ask_price = QTableWidgetItem(str(tick.askPrice1))
        cell_ask_volume = QTableWidgetItem(str(tick.askVolume1))

        # 将单元格插入表格
        self.setItem(0, 0, cell_time)
        self.setItem(0, 1, cell_symbol)
        self.setItem(0, 2, cell_last_price)
        self.setItem(0, 3, cell_bid_volume)
        self.setItem(0, 4, cell_bid_price)
        self.setItem(0, 5, cell_ask_price)
        self.setItem(0, 6, cell_ask_volume)
        
        #logging.info(','.join([t, log]))

class TradingMonitor(QWidget):

    signal = pyqtSignal(type(Event()))
    def __init__(self,eventEngine,mainEngine,parent=None):
        """Constructor"""
        super(TradingMonitor, self).__init__(parent)

        self.__eventEngine = eventEngine
        self.__mainEngine = mainEngine
        self.init_ui()
        self.signal.connect(self.update_tick)
        self.__eventEngine.register(EVENT_TICK, self.signal.emit)

    def init_ui(self):
        self.setWindowTitle('交易')
        form_layout = QFormLayout()
        self.edit_0 = QLineEdit()
        form_layout.addRow("交易所:",self.edit_0)

        self.edit_1 = QLineEdit()
        form_layout.addRow('订阅代码:',self.edit_1)
        self.edit_1.returnPressed.connect(self.subscribe)
        

        self.t_label = QLabel()
        self.symbol_label = QLabel()
        self.symbol_label.setAlignment(Qt.AlignRight)
        form_layout.addRow(self.t_label,self.symbol_label)

        self.ap_label = QLabel()
        self.av_label = QLabel()
        self.av_label.setAlignment(Qt.AlignRight)
        form_layout.addRow(self.ap_label,self.av_label)

        self.lp_label = QLabel()
        form_layout.addRow(self.lp_label)

        self.bp_label = QLabel()
        self.bv_label = QLabel()
        self.bv_label.setAlignment(Qt.AlignRight)
        form_layout.addRow(self.bp_label,self.bv_label)

        self.setLayout(form_layout)

    def subscribe(self):
        symbol = self.edit_1.text()
        self.__mainEngine.subscribe(symbol)

    def update_tick(self,event):

        t = datetime.now()
        t = t.strftime('%H:%M:%S')
        tick = event.dict_['data']

        self.t_label.setText(t)
        self.symbol_label.setText(tick.symbol)
        self.ap_label.setText(str(tick.askPrice1))
        self.av_label.setText(str(tick.askVolume1))
        self.lp_label.setText(str(tick.lastPrice))
        self.bp_label.setText(str(tick.bidPrice1))
        self.bv_label.setText(str(tick.bidVolume1))

if __name__ == "__main__":
    event_engine = EventEngine()
    app = QApplication([])
    ex = MainWindow(event_engine)
    ex.showMaximized()
    app.exec()

