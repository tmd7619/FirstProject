from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# class UserRegister (models.Model):
#     user_id = models.CharField(max_length=50)
#     user_pwd = models.CharField(max_length=50)
#     user_name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.user_id+" , "+self.user_pwd+" , "+self.user_name

class Quiz(models.Model):
    classType = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    explanation = models.TextField()
    answer = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    regdate = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title
