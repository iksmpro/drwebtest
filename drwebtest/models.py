from django.db import models

class Task(models.Model):
    create_time = models.DateTimeField('Creation time')
    finish_time = models.DateTimeField('Finish time', null=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        status_str = ['IN QUEUE', 'RUNNING', ('FINISHED at %s' % self.finish_time)][self.status]
        self.str_repr = "Task<{task_id}> ({additional}), created at {creation}".format(task_id=self.id, additional=status_str, creation=self.create_time)
        return self.str_repr 
