from django.db import models

# Create your models here.



# DEPARTMENT MODEL
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.CharField(max_length=300, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  

    def __str__(self):
        return self.name



# ROLE MODEL
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name



# MANAGER MODEL
class Manager(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# USER MODEL
class Users(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=100)
    dept_id = models.ForeignKey(Department, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)
    reporting_manager = models.ForeignKey(Manager, null=True, blank=True, on_delete=models.SET_NULL)
    date_of_joining = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username  


