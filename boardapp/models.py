from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# class UserRegister(models.Model) :
#     user_id = models.CharField(max_length=50)
#     user_pwd= models.CharField(max_length=50)
#     user_email= models.CharField(max_length=50)
#
#     bio = models.TextField(max_length=500, blank=True)
#     contact = models.CharField(max_length=50, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#
#     profile_img= models.ImageField(null=True)
#
#     def __str__(self):
#         return self.user_id+", "+self.user_pwd+", "+self.user_email
#
#     photo= models.ImageField(blank=True)



class Question(models.Model):
        modify_date = models.DateTimeField(null=True, blank=True)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        subject = models.CharField(max_length=200)
        content = models.TextField(max_length=200)
        create_date = models.DateTimeField(default=timezone.now())
        voter = models.ManyToManyField(User, related_name='voter_question') # voter 추가
        def __str__(self):
                return self.subject

class Answer(models.Model):
        modify_date = models.DateTimeField(null=True, blank=True)
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        content = models.TextField(max_length=200)
        create_date = models.DateTimeField(default=timezone.now())
        voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        content = models.TextField()
        create_date = models.DateTimeField()
        modify_date = models.DateTimeField(null=True, blank=True)
        question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
        answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)



