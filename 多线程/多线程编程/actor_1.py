from collections import deque


class ActorScheduler:
    def __init__(self):
        self._actors = {}
        self._msg_queue = deque()

    def new_actor(self, name, actor):
        self._msg_queue.append((actor, None))
        self._actors[name] = actor

    def sendMsg(self, name, msg):
        actor = self._actors[name]
        if actor:
            self._msg_queue.append((actor, msg))

    def run(self):
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration:
                pass


if __name__ == "__main__":
    def printer():
        while True:
            msg = yield
            print("get: ", msg)


    def counter(sched):
        while True:
            n = yield
            if n == 0:
                break
            sched.sendMsg("printer", n)
            sched.sendMsg("counter", n - 1)

    sched = ActorScheduler()
    sched.new_actor("printer", printer())
    sched.new_actor("counter", counter(sched))
    sched.sendMsg("counter", 100)
    sched.run()