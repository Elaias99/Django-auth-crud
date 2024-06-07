from django.contrib import admin
from .models import Task

#Registrar el modelo Task en el sitio de administración de Django.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(Task, TaskAdmin)