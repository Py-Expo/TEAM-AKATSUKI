from django.db import models


class Touch(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    message = models.TextField(max_length=30)

class newsletter(models.Model):
    email = models.EmailField(default='none')