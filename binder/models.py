from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Binder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)