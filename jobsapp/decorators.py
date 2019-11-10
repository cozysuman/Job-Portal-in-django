from django.core.exceptions import PermissionDenied
from jobsapp.models import Company
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render


def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'employee':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap

def user_is_superuser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap

def user_can_search(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser or user.role == 'employer' :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap

def company_can_post(function):
    def wrap(request, *args, **kwargs):
            
        try:
            company = Company.objects.get(user= request.user)
        except Company.DoesNotExist:
            return render(request,'Errors/apply_here.html')
        else:
            if company.registered :
                return function(request, *args, **kwargs)
                
            else:
                return render(request,'Errors/request_submitted.html')
                

    return wrap

# def company_can_post(function):
#     def wrap(request, *args, **kwargs):
#         company = Company.objects.get(user= request.user)
#         if company.registered :
#             return function(request, *args, **kwargs)
        
#         else:
#             return HttpResponse("sorry!")


#     return wrap