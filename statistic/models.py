from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=32, null=True)
    mobile = models.CharField(max_length=11, null=True)
    introduction = models.TextField()
    table_count = models.IntegerField(default=0)


class UserTable(models.Model):
    filename = models.CharField(max_length=64)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    fileid = models.IntegerField()
