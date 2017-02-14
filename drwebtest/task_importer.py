from multiprocessing import Process
from django.utils import timezone

from .models import Task
from . import this_module_name

def worker(queue, task):
    __import__(this_module_name + '.static.test', fromlist=[''])
    queue.put({"status":1, "message":"complete", "time":timezone.now(), "task": task})

class QueueManager:
    def __init__(self, queue, max_tasks=2):
        self.max_tasks = max_tasks
        self.queue = queue
        self.now_running = 0
        self.max_tasks = max_tasks
        self.running_tasks = set()

    def do_stuff(self):
        while True:
            tasks_in_queue = list(Task.objects.filter(status__in=(0,1)).exclude(id__in=self.running_tasks)[:self.max_tasks-self.now_running])
            while len(tasks_in_queue) and self.now_running < self.max_tasks:
                task = tasks_in_queue.pop(0)
                task.status = 1
                task.finish_time = timezone.now()
                task.save()
                proc = Process(target=worker, args=(self.queue, task))
                self.now_running += 1
                self.running_tasks.add(task.id)
                proc.start()
            answer = self.queue.get()
            if answer['status']:
                self.now_running -= 1
                answer['task'].status = 2
                answer['task'].finish_time = answer['time']
                answer['task'].save()
                self.running_tasks.discard(answer['task'].id)

