import sys
#sys模块提供了与Python解释器和操作系统交互的功能
from PyQt5.QtCore import Qt
#设置窗口的标题栏图标、文本对齐方式、鼠标光标形状、键盘事件处理等等
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QGroupBox,QRadioButton,QGridLayout,QLineEdit,  QFormLayout
#QApplication是用于管理应用程序的类，而QWidget是用于创建窗口和用户界面的类,QPushButton按钮类,QVBoxLayout表垂直布局
class MyWindow(QWidget):
#MyWindow的自定义窗口类，该类继承自PyQt5中的QWidget类
    def __init__(self):
    #构造方法的定义，其中 self 参数表示当前对象的实例。构造方法是在创建一个新的MyWindow类实例时自动调用的
        super().__init__()
        #确保在MyWindow对象初始化时QWidget类的构造方法得到调用，从而正确地初始化窗口对象。
        self.init_ui()
        #初始化用户界面(UI)中的各种部件和设置。用于在创建窗口或部件的时候执行一些初始化操作，以确保UI的正确设置

    def init_ui(self):
        self.resize(400,400)
        #将窗口的初始大小设置为400x400像素
        self.setWindowTitle("登录")
        #将窗口名字设置为“计算器”

        external= QVBoxLayout()
        #创建一个最外层垂直布局对象
        form_layout = QFormLayout()
        #创建一个表单布局器
        self.edit=QLineEdit()
        #创建一个编辑框
        self.edit.setPlaceholderText('请输入账号')
        #设置了占位文本为 "请输入账号"
        form_layout.addRow('账号：',self.edit)
        #表单布局中添加一行。通常需要两个参数：一个标签和一个小部件本代码中，标签是字符串'账号：'，小部件由变量edit表示。
        self.edit2 = QLineEdit()
        # 创建一个编辑框
        self.edit2.setPlaceholderText('请输入密码')
        
        # 设置了占位文本为 "请输入密码"
        form_layout.addRow('密码：', self.edit2)
        # 表单布局中添加一行。通常需要两个参数：一个标签和一个小部件本代码中，标签是字符串'密码：'，小部件由变量edit2表示。
        external.addLayout(form_layout)
        # 将form_layout添加到external中
        bin=QPushButton('登录')
        bin.clicked.connect(self.login)
        #创建登录按钮
        external.addWidget(bin,alignment=Qt.AlignCenter)
        #将按钮加入到external中，并设置对齐方式
        self.setLayout(external)
        #设置窗口显示为external窗口
        
    def login(self):
        acount = self.edit.text()
        password = self.edit2.text()
        print(f"账号：{acount} ，密码：{password}")
        

if __name__ =='__main__':
# 检查Python脚本是否正在作为主程序直接运行
    app = QApplication(sys.argv)
    #创建一个APP对象，sys.argv是一个包含命令行参数的列表，用于从命令行接收参数
    w=MyWindow()
    #意味着你可以使用变量w来引用和操作这个窗口
    w.show()
    #显示窗口
    app.exec_()
    #用于启动事件循环。事件循环负责处理用户输入、绘制界面、处理事件、触发信号等等。只有在事件循环运行时，你的应用程序才能够响应用户的操作。
