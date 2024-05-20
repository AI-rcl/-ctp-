from test01 import MainWindow
from event_engine import Event,EventEngine
from event import *
import time
from threading import Timer
from PyQt5.QtWidgets import QApplication

class TestEngine(object):

    def __init__(self,engine) -> None:
        self.engine = engine

    def put_tick(self):
        count = 0

        while count <= 100:
            event = Event(type_=EVENT_TICK)
            event.dict_['tick'] = f'tick_{count}'
            self.engine.put(event)
            time.sleep(1)
            count += 1


def test():
    event_engine = EventEngine()
    app = QApplication([])
    ex = MainWindow(event_engine)
    ex.showMaximized()
    test_engin = TestEngine(event_engine)
    timer = Timer(1,test_engin.put_tick)
    timer.start()
    app.exec()


if __name__ == "__main__":
    test()