import threading
import asyncio

@asyncio.coroutine
def hello(i):
    print('Hello world! (%s) (%s)' % (i, threading.currentThread()))
    yield from asyncio.sleep(1)
    print('Hello again! (%s) (%s)' % (i, threading.currentThread()))

loop = asyncio.get_event_loop()
tasks = [hello(1), hello(2), hello(3)]
print('Main start')
loop.run_until_complete(asyncio.wait(tasks))
print('Main end')
loop.close()
