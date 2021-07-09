from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, RegisterForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import Orderfilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .c_decorators import authenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# Create your views here.
@authenticated_user
def LogIn(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=uname, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Incorrect Username or password.")
            return redirect('log_in')
    return render(request, 'analog/login_page.html')


@authenticated_user
def Register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            messages.success(request, "Account created for: " + user_name)
            user = form.save()
            return redirect('log_in')
    context = {
        'form': form,
    }
    return render(request, 'analog/sign_up_page.html', context)


def LogOut(request):
    logout(request)
    return redirect('log_in')


@login_required(login_url='log_in')
# @allowed_users(allowed_roles=['Admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    amounts = {
        'total': Order.objects.all().count(),
        'delivered': Order.objects.filter(status='Delivered').count(),
        'pending': Order.objects.filter(status="Pending").count(),
        'out': Order.objects.filter(status="Out for delivery").count(),
    }
    context = {
        'order': orders,
        'customer': customers,
        'amounts': amounts,

    }
    return render(request, "analog/dashboard.html", context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    product = Product.objects.all()
    context = {
        "product": product
    }
    return render(request, "analog/products.html", context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=['Admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    o_length = order.count()
    myFilter = Orderfilter(request.GET, queryset=order)
    order = myFilter.qs
    context = {
        'customer': customer,
        'order': order,
        'len': o_length,
        'myFilter': myFilter,
    }
    return render(request, 'analog/customer.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=['Admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none())
    # form=OrderForm(initial={'customer':customer,})
    context = {'formset': formset, 'customer': customer}
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, "analog/order_form.html", context)


@login_required(login_url='log_in')
# @allowed_users(allowed_roles=['Admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    cont = {'update_form': form}
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request,'analog/update_order.html',cont)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=['Admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'analog/order_delete.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles='Customer')
def UserPage(request):
    orders = request.user.customer.order_set.all()
    amounts = {
        'total': request.user.customer.order_set.all().count(),
        'delivered': request.user.customer.order_set.filter(status='Delivered').count(),
        'pending': request.user.customer.order_set.filter(status='Pending').count(),
        'out': request.user.customer.order_set.filter(status='Out for delivery').count(),
    }
    context = {
        'orders': orders,
        'amounts': amounts
    }
    return render(request, 'analog/user.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles='Customer')
def settingProfile(request):
    form = CustomerForm(instance=request.user.customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('user_setting')
    context = {
        'form': form,
    }
    return render(request, 'analog/setting.html', context)
