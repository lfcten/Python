from queue import Queue
from threading import Thread, Event

# Sentinel used for shutdown
class ActorExit(Exception):
    pass
#
class Actor:
    def __init__(self):
        self._mailbox = Queue()

    def send(self, msg):
        '''
        Send a message to the actor
        '''
        self._mailbox.put(msg)

    def recv(self):
        '''
        Receive an incoming message
        '''
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        '''
        Close the actor, thus shutting it down
        '''
        self.send(ActorExit)

    def start(self):
        '''
        Start concurrent execution
        '''
        self._terminated = Event()
        t = Thread(target=self._bootstrap)

        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        '''
        Run method to be implemented by the user
        '''
        while True:
            msg = self.recv()

# Sample ActorTask
# class PrintActor(Actor):
#     def run(self):
#         while True:
#             msg = self.recv()
#             print('Got:', msg)
#
# # Sample use
# p = PrintActor()
# p.start()
# p.send('Hello')
# p.send('World')
# p.close()
# p.join()

# from threading import Event
# class Result:
#     def __init__(self):
#         self._evt = Event()
#         self._result = None
#
#     def set_result(self, value):
#         self._result = value
#
#         self._evt.set()
#
#     def result(self):
#         self._evt.wait()
#         return self._result
#
# class Worker(Actor):
#     def submit(self, func, *args, **kwargs):
#         r = Result()
#         self.send((func, args, kwargs, r))
#         return r
#
#     def run(self):
#         while True:
#             func, args, kwargs, r = self.recv()
#             r.set_result(func(*args, **kwargs))
#
# # Example use
# worker = Worker()
# worker.start()
# r = worker.submit(pow, 2, 3)
# print(r.result())


from collections import deque


def countdown(n):
    while n > 0:
        print('T-minus', n)
        yield
        n -= 1
    print('Blastoff!')

def countup(n):
    x = 0
    while x < n:
        print('Counting up', x)
        yield
        x += 1


class TaskScheduler:
    def __init__(self):
        self._task_queue = deque()

    def new_task(self, task):
        '''
        Admit a newly started task to the scheduler

        '''
        self._task_queue.append(task)

    def run(self):
        '''
        Run until there are no more tasks
        '''
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                # Run until the next yield statement
                next(task)
                self._task_queue.append(task)
            except StopIteration:
                # Generator is no longer executing
                pass

# Example use
sched = TaskScheduler()
sched.new_task(countdown(10))
sched.new_task(countdown(5))
sched.new_task(countup(15))
sched.run()