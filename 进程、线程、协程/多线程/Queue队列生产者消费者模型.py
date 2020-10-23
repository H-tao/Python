""" 生产者每隔3秒加入一个值，消费者不断从队列取值 """
import threading
from queue import Queue
import time


# 每隔3秒加入一个值
def set_value(q: Queue):
    index = 0
    while True:
        q.put(index, block=True)
        index += 1
        time.sleep(1)


def get_value(q: Queue):
    while True:
        print(q.get(block=True))


if __name__ == '__main__':
    q = Queue(maxsize=5)
    t1 = threading.Thread(target=set_value, args=(q, ))
    t2 = threading.Thread(target=get_value, kwargs={'q': q})
    t1.start()
    t2.start()
