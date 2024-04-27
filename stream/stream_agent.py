from multiprocessing import Process, Queue
import time


class StreamAgent:
    def __init__(self):
        self.q = Queue()

    # change this into the real task
    def stream_task(self, *args, **kwargs):
        print(f"stream_task starts with args {args}, kwargs {kwargs}")
        t = 0
        while True:
            self.q.put([t] * 10)
            t += 1
            time.sleep(1)

    def start(self):
        p = Process(target=self.stream_task, args=(1, 2, 3), kwargs={'arg1': 1, 'arg2': 2})
        p.start()

    def fetch(self):
        result = []

        while not self.q.empty():
            result.append(self.q.get(block=False))

        return result


if __name__ == '__main__':
    agent = StreamAgent()
    agent.start()

    while True:
        print("Fetch!")
        print(agent.fetch())
        time.sleep(5)
