from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory


# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    d = Order.objects.filter(status="Delivered")
    context = {
        'order': orders,
        'customer': customers,
        'delevered': d,
        'pending': Order.objects.filter(status="Pending"),
        'out': Order.objects.filter(status="Out for delivery")

    }
    return render(request, "analog/dashboard.html", context)


def products(request):
    product = Product.objects.all()
    context = {
        "product": product
    }
    return render(request, "analog/products.html", context)


def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    o_length = order.count()
    context = {
        'customer': customer,
        'order': order,
        'len': o_length
    }
    return render(request, 'analog/customer.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none())
    # form=OrderForm(initial={'customer':customer,})
    context = {'formset': formset, 'customer': customer}
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        print(formset)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, "analog/order_form.html", context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {'form': form}
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'analog/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {'order': order}
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'analog/order_delete.html', context)
