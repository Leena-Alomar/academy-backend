from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_name=models.CharField(max_length=50)
    course_description=models.TextField(max_length=250)
    course_time= models.CharField(max_length=50)
    class_date=models.CharField(max_length=50)

    
      
    def __str__(self):
        return self.course_name


class Schedule(models.Model):
    schedule_name = models.CharField(max_length=50)
    course_related=models.ForeignKey(Course,on_delete=models.CASCADE)

     
    def __str__(self):
        return self.schedule_name

class Lesson(models.Model):
    lesson_name=models.CharField(max_length=50)
    lesson_time=models.CharField(max_length=50)
    lesson_week=models.CharField(max_length=50)
    lesson_brief=models.TextField()
    lesson_sch=models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='lessons')
    
    def __str__(self):
        return self.lesson_name