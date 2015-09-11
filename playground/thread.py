import threading
import Queue
import time

exit = False
size = 10
q = Queue.Queue(size)
proc = False

def prod(q):
    while not exit:
        for i in range(0, size):
            q.put(i)
            print('Put: %d size: %d' % (i, q.qsize()))
        q.join()

t = threading.Thread(target=prod, args=(q,))
t.start()

try:
    while True:
        while not q.full():
            time.sleep(1)
       
        print('Queue is full, prcessing...') 
        while not q.qsize() == 0:
            i = q.get()
            print('Process: %d size: %d' % (i, q.qsize()))
            time.sleep(1)
            q.task_done()
except KeyboardInterrupt:
    exit = True
    while not q.qsize() == 0:
        q.get()
        q.task_done()
    time.sleep(1)
