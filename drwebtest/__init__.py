# from multiprocessing import Queue
# from .task_importer import QueueManager

this_module_name = __loader__.name
public_queue = None #Queue()
manager = None #QueueManager(public_queue)
# we cannot define this variables here, because of django structure. it defined in .urls.startup_code