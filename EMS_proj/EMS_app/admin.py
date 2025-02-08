from django.contrib import admin
from .models import Department, Manager

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)  



@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email', 'department')

