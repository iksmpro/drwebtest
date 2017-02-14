"""drwebtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^newtask/', views.create_new_task),
    url(r'^tasks', views.schedule_page),
    url(r'^.*$', views.main_page),
]

def startup_code():
    from multiprocessing import Queue, Process
    from .task_importer import QueueManager
    from . import this_module_name
    this_module = __import__(this_module_name)
    this_module.public_queue = Queue()
    this_module.manager = QueueManager(this_module.public_queue)
    proc = Process(target=this_module.manager.do_stuff)
    proc.start()

startup_code()  # we need to execute this code only one time, when application starts. 