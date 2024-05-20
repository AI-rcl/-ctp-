from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    """主窗口"""
    # signal = pyqtSignal(type(Event()))
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(MainWindow, self).__init__()

        self.widgetDict = {}    # 用来保存子窗口的字典
        
        self.initUi()
    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle("CTP DEMO——基于vnpy的ctp接口")
        self.setWindowIcon(QIcon('resource/fs.ico'))
        
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

if __name__ == "__main__":
    app = QApplication([])
    ex = MainWindow()
    ex.showMaximized()
    app.exec()

