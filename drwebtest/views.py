from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q


from .models import Task
from . import this_module_name

this_module = __import__(this_module_name)

def calc_last_update(tasks):
    new_time = max(
        max(
            task.create_time,
            (task.finish_time if task.finish_time else task.create_time)
        )
        for task in tasks
    ) if tasks else 0
    return new_time.strftime('%Y-%m-%d %H:%M:%S.%f')

def main_page(request):
    tasks = Task.objects.order_by('-create_time').all()
    new_time = calc_last_update(tasks)
    all(task.__str__() for task in tasks)
    return render(request, 'list.html', {'tasks': tasks, "new_time": new_time})

def schedule_page(request):
    try:
        curtime = request.GET['time']
        tasks = Task.objects.filter(Q(create_time__gt=curtime) | Q(finish_time__gt=curtime)).all()
        new_time = calc_last_update(tasks)
        tasks = [{"id": task.id, "str_repr": task.__str__()} for task in tasks]
    except:
        return JsonResponse({'status':'error'})
    return JsonResponse({'status':'ok', 'tasks': tasks, "new_time": new_time})

def create_new_task(request):
    new_task = Task(create_time=timezone.now())
    new_task.save()
    this_module.public_queue.put({"status":0, "message":"wake up"})
    return JsonResponse({'status':'ok'})
