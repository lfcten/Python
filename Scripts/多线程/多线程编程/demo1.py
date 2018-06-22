# coding = utf-8
# Code to execute in an independent thread
# import threading, functools
# import time
#
# def async(wrapped):
#     def wrapper(*args, **kwargs):
#         t = threading.Thread(target=wrapped, args=args, kwargs=kwargs)
#         # t.daemon = True
#         t.start()
#
#     functools.update_wrapper(wrapper, wrapped)
#     return wrapper
#
# import threading, struct
#
# class Writer:
#
#     @async
#     def write(self, fout, string, blockSize):
#         for block in self.splitToBlock(string, blockSize):
#             header=struct.pack("!i", len(block))
#             fout.write(header)
#             fout.write(block)
#             fout.write(b'\n')
#             fout.flush()
#
#     def splitToBlock(self, string, blockSize):
#         data=string.encode("utf-8")
#         for i in range(0, len(data), blockSize):
#             yield data[i:i+blockSize]
#
# writer = Writer()
# s = time.time()
# writer.write(open("fout1.txt", 'wb'), '1' * 10000000, 2)
# e = time.time()
# time.sleep(10)


import threading
from contextlib import contextmanager

_local = threading.local()


@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        print("release")
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


# The philosopher thread
def philosopher(left, right):
    while True:
        with acquire(left, right):
            print(threading.currentThread(), 'eating')


# The chopsticks (represented by locks)
NSTICKS = 2
chopsticks = [threading.Lock() for n in range(NSTICKS)]

# Create all of the philosophers
for n in range(NSTICKS):
    t = threading.Thread(target=philosopher,
                         args=(chopsticks[n], chopsticks[(n + 1) % NSTICKS]))
    t.start()
