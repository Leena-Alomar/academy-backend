from django.contrib import admin
from .models import Course,Schedule,Lesson

# Register your models here.
admin.site.register(Course)
admin.site.register(Schedule)
admin.site.register(Lesson)