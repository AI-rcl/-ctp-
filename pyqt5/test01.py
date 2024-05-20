from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from event_engine import Event,EventEngine
from event import *
import os
from datetime import date,datetime
import logging 



class MainWindow(QMainWindow):
    """主窗口"""
    # signal = pyqtSignal(type(Event()))
    #----------------------------------------------------------------------
    def __init__(self,even_engine):
        """Constructor"""
        super(MainWindow, self).__init__()

        self.widgetDict = {}    # 用来保存子窗口的字典
        self.ee = even_engine

        self.ee.start()
        self.initUi()
    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle("CTP DEMO——基于vnpy的ctp接口")
        self.setWindowIcon(QIcon('resource/fs.ico'))
        text_edit = QTextEdit()
        self.setCentralWidget(text_edit)
        
        #widgetLogM, dockLogM = self.createDock(LogMonitor, '日志', Qt.RightDockWidgetArea, engine=self.ee, floatable=True)
        widgetTest, dockTest = self.createDock(TestMonitor,'交易',Qt.LeftDockWidgetArea,engine=self.ee,floatable= True)

        # dockLogM.raise_()
        # dockLogM.setMinimumSize(1000,200)
        # #dockLogM.adjustSize()
        # dockLogM.setAllowedAreas(Qt.NoDockWidgetArea)
        
        dockTest.raise_()
        dockTest.setMaximumSize(500,800)
        dockTest.setMinimumSize(300,600)
        dockTest.setAllowedAreas(Qt.NoDockWidgetArea)


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
            #widget = widgetClass(self.ee, engine) if engine else widgetClass(self.ee) 
            widget = widgetClass(engine)
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

class LogMonitor(QTableWidget):
    """用于显示日志"""
    signal = pyqtSignal(type(Event()))
    #----------------------------------------------------------------------
    def __init__(self,eventEngine,parent=None):
        """Constructor"""
        super(LogMonitor, self).__init__(parent)
        self.__eventEngine = eventEngine
        self.setWindowTitle('行情')
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['时间','合约', '最新价','买一量','买一价','卖一价','卖一量'])
        #self.verticalHeader().setVisible(False)                 # 关闭左边的垂直表头
        self.setEditTriggers(QTableWidget.NoEditTriggers) # 设为不可编辑状态
        # self.setColumnWidth(0, 80)
        # self.setColumnWidth(1, 80)
        # Qt图形组件的GUI更新必须使用Signal/Slot机制，否则有可能导致程序崩溃
        # 因此这里先将图形更新函数作为Slot，和信号连接起来
        # 然后将信号的触发函数注册到事件驱动引擎中
        self.signal.connect(self.updateLog)
        self.__eventEngine.register(EVENT_TICK, self.signal.emit)
        self.insertRow(0)
        #保存日志到文件
        path = os.getcwd()+'/vnpy_engine_test/pyqt5/log/eventLog{date}'.format(date=date.today())
        logging.basicConfig(filename=path, level=logging.INFO)
    #----------------------------------------------------------------------
    def updateLog(self, event):
        """更新日志"""
        # 获取当前时间和日志内容
        t = datetime.now()
        print(t)
        t = t.strftime('%H:%M:%S')
        tick = event.dict_['tick']
        # 在表格最上方插入一行
       
        # 创建单元格
        #['时间','合约', '最新价','买一量','买一价','卖一价','卖一量']
        cell_time = QTableWidgetItem(t)
        cell_symbol = QTableWidgetItem(tick)
        # cell_last_price = QTableWidgetItem(tick.last_price)
        # cell_bid_volume = QTableWidgetItem(tick.bidVolume1)
        # cell_bid_price = QTableWidgetItem(tick.bidPrice1)
        # cell_ask_price = QTableWidgetItem(tick.askPrice1)
        # cell_ask_volume = QTableWidgetItem(tick.askVolume1)

        # 将单元格插入表格
        self.setItem(0, 0, cell_time)
        self.setItem(0, 1, cell_symbol)
        # self.setItem(0, 2, cell_last_price)
        # self.setItem(0, 1, cell_bid_volume)
        # self.setItem(0, 1, cell_bid_price)

        # self.setItem(0, 1, cell_ask_price)
        # self.setItem(0, 1, cell_ask_volume)
        
        #logging.info(','.join([t, log]))

class TestMonitor(QWidget):
    """用于显示日志"""
    signal = pyqtSignal(type(Event()))
    #----------------------------------------------------------------------
    def __init__(self,eventEngine,parent=None):
        """Constructor"""
        super(TestMonitor, self).__init__(parent)

        self.__eventEngine = eventEngine
        self.init_ui()

        self.signal.connect(self.update_market)
        self.__eventEngine.register(EVENT_TICK, self.signal.emit)
        

    def init_ui(self):
        self.setWindowTitle('交易')

        #external= QVBoxLayout()
        #创建一个最外层垂直布局对象
        form_layout = QFormLayout()
        #创建一个表单布局器
        self.edit=QLineEdit()
        #创建一个编辑框
        self.edit.setPlaceholderText('输入交易所代码')
        #设置了占位文本为 "输入交易所代码"

        form_layout.addRow('交易所：',self.edit)
        #表单布局中添加一行。通常需要两个参数：一个标签和一个小部件本代码中，标签是字符串'账号：'，小部件由变量edit表示。
        self.edit2 = QLineEdit()
        # 创建一个编辑框

        self.edit2.setPlaceholderText('输入合约代码')
        self.edit2.returnPressed.connect(self.return_press)
        # 设置了占位文本为 "请输入密码"
        form_layout.addRow('代码：', self.edit2)

        self.time_label = QLabel()
        self.ap_label = QLabel()
        self.ap_label.setAlignment(Qt.AlignRight)
        form_layout.addRow(self.time_label,self.ap_label)

        self.setLayout(form_layout)
    
    def return_press(self):
        symbol = self.edit2.text()
        print(symbol)
    
    def update_market(self,event):
        t = datetime.now()
        t = t.strftime('%H:%M:%S')
        tick = event.dict_['tick']
        self.time_label.setText(t)
        self.ap_label.setText(tick)

if __name__ == "__main__":
    event_engine = EventEngine()
    app = QApplication([])
    ex = MainWindow(event_engine)
    ex.showMaximized()
    app.exec()

