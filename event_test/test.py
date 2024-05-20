# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 13:50:45 2018

@author: 18665
"""

# encoding: UTF-8
import sys
from datetime import datetime
from threading import *
#sys.path.append('D:\\works\\TestFile')
#print(sys.path)
from event_manager import *
import time


#事件名称 新文章
EVENT_ARTICAL = "Event_Artical"

#事件源 公众号
class PublicAccounts:
    def __init__(self,eventManager):
        self.__eventManager = eventManager

    def WriteNewArtical(self):
    #事件对象，写了新文章
        count = 10
        while count >=0:
            event = Event(type_=EVENT_ARTICAL)
            event.dict["artical"] = f'如何写出更优雅的代码{count}'

            #发送事件
            self.__eventManager.SendEvent(event)
            print(f'公众号发送新文章{count}')
            count -= 1
            time.sleep(1)
    


#监听器 订阅者
class Listener:
    def __init__(self,username):
        self.__username = username

 #监听器的处理函数 读文章
    def ReadArtical(self,event):
        print(u'%s 收到新文章' % self.__username)
        print(u'正在阅读新文章内容：%s' % event.dict["artical"])

"""测试函数"""
#--------------------------------------------------------------------
def test():
    # 实例化监听器
    listner1 = Listener("thinkroom") #订阅者1
    listner2 = Listener("steve")  #订阅者2
    # 实例化事件操作函数
    eventManager = EventManager()

    #绑定事件和监听器响应函数(新文章)
    eventManager.AddEventListener(EVENT_ARTICAL, listner1.ReadArtical)
    eventManager.AddEventListener(EVENT_ARTICAL, listner2.ReadArtical)
    # 启动事件管理器,# 启动事件处理线程
    eventManager.Start()
 
    publicAcc = PublicAccounts(eventManager)
    timer = Timer(1, publicAcc.WriteNewArtical)
    timer.start()

if __name__ == '__main__':
 test()