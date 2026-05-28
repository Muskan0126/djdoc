from django.db import models
from django.conf import settings

class todolist(models.Model):
    title = models.CharField(max_length =  200)
    description = models.TextField(null = True, blank = True)
    completed = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, default= None)
    def __str__(self):
        return self.title
    class Meta:

        unique_together = (
            'user',
            'title'
        )