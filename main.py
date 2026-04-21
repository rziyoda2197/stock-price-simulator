from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading

class ThreadPoolManager:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.queue = Queue()

    def submit_task(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            func, args, kwargs = task
            self.executor.submit(func, *args, **kwargs)
            self.queue.task_done()

    def shutdown(self):
        self.queue.put(None)
        self.executor.shutdown(wait=True)

def example_task(x, y):
    print(f"Task {x} + {y} = {x + y}")

manager = ThreadPoolManager(5)
manager.submit_task(example_task, 1, 2)
manager.submit_task(example_task, 3, 4)
manager.submit_task(example_task, 5, 6)
manager.start()
manager.shutdown()
```

Kodda quyidagilar mavjud:

*   `ThreadPoolManager` klassi yaratildi, u quyidagilar bilan ishlaydi:
    *   `max_workers` parametrini qabul qiladi, bu thread pooldagi ishchi threadlar soni.
    *   `submit_task` metodi orqali tasklarni qo'shish uchun queue qo'llaniladi.
    *   `start` metodi orqali thread poolni boshlash uchun thread yaratiladi.
    *   `run` metodi orqali tasklarni ishga tushirish uchun executor qo'llaniladi.
    *   `shutdown` metodi orqali thread poolni to'xtatish uchun executor va queue qo'llaniladi.
*   `example_task` funktsiyasi yaratildi, u 2 sonni qo'shadi va natijani konsolga chiqaradi.
*   `ThreadPoolManager` klassi yaratildi va 5 ishchi threadlari bilan ishga tushirildi.
*   3 task qo'shildi va thread poolni boshlash uchun start metodi chaqirildi.
*   Thread poolni to'xtatish uchun shutdown metodi chaqirildi.
