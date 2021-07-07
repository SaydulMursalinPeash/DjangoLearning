from django.http import HttpResponse
from django.shortcuts import redirect


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decoretor(view_func):
        def wraper_function(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("you are not authorised to view this page..")

        return wraper_function

    return decoretor


def admin_only(view_func):
    def wraper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Customer':
            return redirect('user_page')
        if group == 'Admin':
            return view_func(request, *args, **kwargs)
    return wraper_func
