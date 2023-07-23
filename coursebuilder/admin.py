from django.contrib import admin
from django.db import models
from .models import Course, Events, UserProfile, Grade, Assignment, MembersName, Video  

# Register your models here.
admin.site.register(Course)
admin.site.register(UserProfile)
admin.site.register(Grade)
admin.site.register(Assignment)
admin.site.register(MembersName)
admin.site.register(Video)
admin.site.register(Events)
