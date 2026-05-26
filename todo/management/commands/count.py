from django.core.management.base import BaseCommand
from todo.models import todolist

# this command counts the total number of todo lists

class Command(BaseCommand):
    def handle(self, *args, **options):
        total = todolist.objects.count()

        return(f"total todo : {total}")