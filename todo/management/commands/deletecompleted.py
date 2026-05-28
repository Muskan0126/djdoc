from django.core.management.base import BaseCommand
from todo.models import todolist

class Command(BaseCommand):
    help = 'delete all the completed task'
    def handle(self, *args, **kwargs):
        completed_tasks = todolist.objects.filter(completed = True)
        countcomp = completed_tasks.count()

        if countcomp == 0:
            self.stdout.write('No task found')
            return
        completed_tasks.delete()

        self.stdout.write(f'{countcomp} task deleted')