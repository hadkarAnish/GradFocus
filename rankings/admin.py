from django.contrib import admin
from .models import City, University, Program, Course, Matches, Student

admin.site.register(City)
admin.site.register(University)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Matches)
admin.site.register(Student)
