from django.urls import path
from EMS_app import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('department_dashboard/', views.department_dashboard, name='department_dashboard'),
    path('create_dept/', views.create_dept, name='create_dept'),
    path('update_dept/<did>/', views.update_dept, name='update_dept'),
    path('delete_dept/<did>/', views.delete_dept, name='delete_dept'),


    path('role_dashboard/', views.role_dashboard, name='role_dashboard'),
    path('create_role/', views.create_role, name='create_role'),
    path('update_role/<rid>/', views.update_role, name='update_role'),
    path('delete_role/<rid>/', views.delete_role, name='delete_role'),


    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('update_employee/<int:eid>/', views.update_employee, name='update_employee'),
    path('delete_employee/<eid>', views.delete_employee, name='delete_employee'),


    path('register/', views.register, name='register'),
    path('login/', views.ulogin, name='ulogin'),
    path('ulogout/', views.ulogout, name='ulogout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

