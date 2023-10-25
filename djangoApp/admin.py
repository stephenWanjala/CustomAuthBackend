from django.contrib import admin

from djangoApp import models

# Register your models here.
admin.site.register(models.Semester)
admin.site.register(models.Unit)
admin.site.register(models.Course)
admin.site.register(models.AcademicYear)
admin.site.register(models.CustomUser)
admin.site.register(models.Student)
admin.site.register(models.Lecturer)
