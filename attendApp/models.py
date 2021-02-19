from django.db import models

# Create your models here.
class StudentUser(models.Model):
    user_name = models.CharField(max_length=10)
    user_nickname = models.CharField(max_length=20)
    user_attend = models.IntegerField(default=0)
    user_absent = models.IntegerField(default=0)

    def __str__(self):
        return self.user_name

class TotalCurriculum(models.Model):
    subject_name = models.CharField(max_length=20)
    subject_spec = models.CharField(max_length=50)
    subject_tutor = models.CharField(max_length=5)
    subject_comp = models.IntegerField(default=100)

    def __str__(self):
        return self.subject_name
    subject_date = models.DateField('date published')

class SpecDetail(models.Model):
    subject = models.ForeignKey(TotalCurriculum, on_delete=models.CASCADE)
    spec_name = models.CharField(max_length=20)

    def __str__(self):
        return self.spec_name + "-" + self.subject.subject_name

class CustomPeriod(models.Model):
    name = models.CharField(max_length=30)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name