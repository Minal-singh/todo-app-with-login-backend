import uuid
from django.db import models
from testapp.models import CustomUser

# Create your models here.


class Todo(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=120)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="todos",null=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
