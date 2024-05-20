from event_engine import EventEngine,Event
from event import EVENT_TICK
import time
from threading import Timer

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

class Strategy:
    
    def __init__(self,name) -> None:
        self.name = name
    
    def get_tick(self,event):
        print(f"收到tick:{event.dict_['tick']}")


def test():

    main_engine = EventEngine()
    rb_tick = Strategy('rb_tick')
    main_engine.start()

    main_engine.register(EVENT_TICK,rb_tick.get_tick)

    test_engin = TestEngine(main_engine)
    timer = Timer(2,test_engin.put_tick)
    timer.start()

if __name__=='__main__':
    test()

