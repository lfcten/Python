import threading
from queue import Queue

# shutdown signal
_sentinel = object()


# producer
def producer(q_pro):
    pass


# consumer
def consumer(q_con):
    pass


q = Queue()
t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))
t1.start()
t2.start()
