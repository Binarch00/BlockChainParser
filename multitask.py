from multiprocessing import Process
import redis
import time


class IndexedTask:

    speed_step = 5000
    speed_in_minutes = False

    def __init__(self, start_index, end_index):
        self.start = start_index
        self.end = end_index
        self.current = start_index
        self.rconn = redis.Redis(host='localhost', port=6379, db=0)
        self.key = "index-task/{}/{}".format(start_index, end_index)
        cur = self.rconn.get(self.key)
        if cur:
            self.start = int(cur)
        self.start_time = time.time()

    def distributed_task(self, index):
        raise NotImplementedError

    def process_speed(self):
        tdiff = time.time() - self.start_time
        if self.speed_in_minutes:
            tdiff = tdiff/60
        self.start_time = time.time()
        print(" speed {}/{}".format(self.speed_step/tdiff, "min" if self.speed_in_minutes else "sec"))

    def run(self):
        for index in range(self.start, self.end + 1):
            self.distributed_task(index)
            if index % 10 == 0:
                self.rconn.set(self.key, index)
            if index % self.speed_step == 0:
                self.process_speed()
        self.rconn.set(self.key, self.end)


class IndexedTaskManager:

    def __init__(self, start, end, task_class: IndexedTask, split=8):
        total = end - start
        step = total//split
        steps = [[step*i + start, step*(i+1) + start - 1] for i in range(0, split)]
        steps[-1][-1] = end
        self.steps = steps
        print("Steps: %s" % steps)
        for st in self.steps:
            st.append(task_class(st[0], st[1]))

    def run(self):
        for st in self.steps:
            st.append(Process(target=st[2].run))
            st[3].start()
        for st in self.steps:
            st[3].join()


if __name__ == "__main__":
    itm = IndexedTaskManager(1, 100000000, IndexedTask)
    itm.run()
