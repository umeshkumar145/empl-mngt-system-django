from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from .models import Employee, Role, Department

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_emp(request):
    # Your view logic here
    return HttpResponse("Employee added")


# Create your views here.
def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'all_emp.html', context)


def add_emp(request, department=None, role=None):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept_id = int(request.POST['dept'])
        role_id = int(request.POST['role'])

        try:
            department = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
        except Department.DoesNotExist:
            return HttpResponse("Invalid Department!")
        except Role.DoesNotExist:
            return HttpResponse("Invalid Role!")

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=department,
            role=role,
            hire_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse("Employee added successfully")
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse('An exception occurred! Employee has not been added!')


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed successfully!")
        except:
            return HttpResponse("Pls Enter a valid Emp ID!")

    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        dept = request.POST.get('dept', None)
        role = request.POST.get('role', None)
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An exception occurred!')
