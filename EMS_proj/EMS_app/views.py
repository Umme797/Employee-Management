from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from EMS_app.models import Role, Department, Users, Manager
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)



# Create your views here.



# REGISTER FUNCTION
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', '').strip()
        email = request.POST.get('uemail', '').strip()
        upass = request.POST.get('upass', '').strip()
        context = {}

        if not uname or not email or not upass:
            context['errmsg'] = "Please fill all the fields."
            return render(request, 'register.html', context)

        if User.objects.filter(username=uname).exists():
            context['errmsg'] = "Username already exists. Please choose a different one."
            return render(request, 'register.html', context)

        if User.objects.filter(email=email).exists():
            context['errmsg'] = "Email ID already exists. Use another Email ID."
            return render(request, 'register.html', context)

        try:
            u = User(username=uname, email=email)
            u.set_password(upass)
            u.save()
            context['successmsg'] = "User registered successfully! Please log in."
            return redirect('ulogin')

        except Exception as e:
            print("Error:", e)
            context['errmsg'] = "An error occurred during registration. Please try again."
            return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')



# LOGIN FUNCTION
def ulogin(request):
    if request.user.is_authenticated:
        return redirect("/department_dashboard")  
    
    if request.method == "POST":  
        uname = request.POST.get('uname', '').strip()
        upass = request.POST.get('upass', '').strip()
        context = {}

        if not uname or not upass: 
            context['errmsg'] = "Please fill all the fields"
            return render(request, 'login.html', context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:  
                login(request, u)
                return redirect("/employee_dashboard")
            else:  
                context['errmsg'] = "Invalid Username/Password!!"
                return render(request, 'login.html', context)

    else: 
        return render(request, 'login.html')



# LOGOUT FUNCTION
def ulogout(request):
    logout(request)
    return redirect('ulogin')



# DEPARTMENT DASHBOARD FUNCTION
@login_required
def department_dashboard(request):
    context = {}
    departments = Department.objects.all()
    context['departments'] = departments
    return render(request, 'department_dashboard.html', context)



# CREATE DEPARTMENT FUNCTION
def create_dept(request):
    context = {}

    if request.method == "POST":
        dname = request.POST.get('dname')
        ddesc = request.POST.get('ddesc')

        context['dname'] = dname
        context['ddesc'] = ddesc

        if Department.objects.filter(name=dname).exists():
            messages.error(request, "Department name already exists.")
        else:
            context['department'] = Department.objects.create(name=dname, description=ddesc)
            messages.success(request, "Department created successfully.")
            return redirect('department_dashboard')

    return render(request, 'create_dept.html', context)



# UPDATE DEPARTMENT FUNCTION
def update_dept(request, did):
    context = {}
    department = get_object_or_404(Department, id=did)
    context['department'] = department

    if request.method == "POST":
        department.name = request.POST.get('dname')
        department.description = request.POST.get('ddesc')
        department.save()
        messages.success(request, "Department updated successfully.")
        return redirect('department_dashboard')

    return render(request, 'update_dept.html', context)



# DELETE DEPARTMENT FUNCTION    
def delete_dept(request, did):
    department = get_object_or_404(Department, id=did)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect('department_dashboard')





# ROLE DASHBOARD FUNCTION
def role_dashboard(request):
    context = {}
    roles = Role.objects.all()
    context['roles'] = roles
    return render(request, 'role_dashboard.html', context)



# CREATE ROLE FUNCTION
@login_required
def create_role(request):
    context = {}

    if request.method == "POST":
        rname = request.POST.get('rname')
        rdesc = request.POST.get('rdesc')

        context['rname'] = rname
        context['rdesc'] = rdesc

        if Role.objects.filter(role_name=rname).exists():
            messages.error(request, "Role name already exists.")
        else:
            context['role'] = Role.objects.create(role_name=rname, description=rdesc)
            messages.success(request, "Role created successfully.")
            return redirect('role_dashboard')

    return render(request, 'create_role.html', context)



# UPDATE ROLE FUNCTION
@login_required
def update_role(request, rid):
    context = {}
    role = get_object_or_404(Role, role_id=rid) 
    context['role'] = role

    if request.method == "POST":
        role.role_name = request.POST.get('rname')
        role.description = request.POST.get('rdesc')
        role.save()
        messages.success(request, "Role updated successfully.")
        return redirect('role_dashboard')

    return render(request, 'update_role.html', context)



# DELETE DEPARTMENT FUNCTION 
@login_required   
def delete_role(request, rid):
    role = get_object_or_404(Role, role_id=rid)
    role.status = False  
    role.delete()
    messages.success(request, "Role deleted successfully.")
    return redirect('role_dashboard')





# EMPLOYEE DASHBOARD FUNCTION
def employee_dashboard(request):
    context = {}
    employees = Users.objects.all()
    context['employees'] = employees
    return render(request, 'employee_dashboard.html', context)



# CREATE EMPLOYEE FUNCTION
def create_employee(request):
    context = {}
    if request.method == "POST":
        first_name = request.POST.get('efname')
        last_name = request.POST.get('elname')
        email = request.POST.get('eemail')
        mobile = request.POST.get('emobile')
        role_name = request.POST.get('erole')
        department_name = request.POST.get('edepartment')
        reporting_manager_email = request.POST.get('emanager') 
        joining_date = request.POST.get('ejoiningDate')
        username = request.POST.get('eusername')
        password = request.POST.get('epass')
        
        hashed_password = make_password(password)

        if Users.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif Users.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            try:
                role = Role.objects.get(role_name=role_name)
            except Role.DoesNotExist:
                messages.error(request, "Selected role does not exist.")
                return redirect('create_employee')

            try:
                department = Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                messages.error(request, "Selected department does not exist.")
                return redirect('create_employee')
            
            try:
                manager = Manager.objects.get(email=reporting_manager_email)
            except Manager.DoesNotExist:
                messages.error(request, "Selected manager does not exist.")
                return redirect('create_employee')

            new_user = Users.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                username=username,
                password=hashed_password,  
                dept_id=department,
                role_id=role,
                reporting_manager_id=manager.id,
                date_of_joining=joining_date
            )
            new_user.save()

            messages.success(request, "Employee created successfully.")
            return redirect('employee_dashboard')

    roles = Role.objects.all()
    departments = Department.objects.all()
    managers = Manager.objects.all()  
    
    context['roles'] = roles
    context['departments'] = departments
    context['managers'] = managers
    
    return render(request, 'create_employee.html', context)



# UPDATE EMPLOYEE FUNCTION
def update_employee(request, eid):
    employee = get_object_or_404(Users, employee_id=eid)

    if request.method == "POST":
        employee.first_name = request.POST.get('efname')
        employee.last_name = request.POST.get('elname')
        employee.email = request.POST.get('eemail')
        employee.mobile = request.POST.get('emobile')
        employee.username = request.POST.get('eusername')

        role_id = request.POST.get('erole')
        dept_id = request.POST.get('edepartment')
        manager_email = request.POST.get('emanager')  

        employee.role_id = Role.objects.get(role_id=role_id)  
        employee.dept_id = Department.objects.get(name=dept_id)
        employee.reporting_manager = Manager.objects.get(email=manager_email) if manager_email else None 
        employee.date_of_joining = request.POST.get('ejoiningDate')

        new_password = request.POST.get('epass')
        if new_password:
            hashed_password = make_password(new_password)
            employee.password = hashed_password 

        employee.save()
        messages.success(request, "Employee updated successfully.")
        return redirect('employee_dashboard')

    roles = Role.objects.all()
    departments = Department.objects.all()
    managers = Manager.objects.all()

    context = {
        'employee': employee,
        'roles': roles,
        'departments': departments,
        'managers': managers,
    }

    context['selected_role'] = employee.role_id.role_id 
    context['selected_department'] = employee.dept_id.name
    context['selected_manager'] = employee.reporting_manager.email if employee.reporting_manager else None

    return render(request, 'update_employee.html', context)



# DELETE EMPLOYEE FUNCTION
def delete_employee(request, eid):
    employees = get_object_or_404(Users, employee_id=eid)   
    employees.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect('employee_dashboard')



