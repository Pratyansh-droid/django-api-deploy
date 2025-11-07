from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default="Unknown Author")

    description = models.TextField(default="No description")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
