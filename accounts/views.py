from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .form import OrderForm, CustomerForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .decorators import unauthorized_user, allowed_user, admin_only
from django.contrib.auth.models import Group
from django.contrib import messages


@unauthorized_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, password=password, username=username)
    if user is not None:
      login(request, user)
      return redirect('/')
    else: 
      messages.info(request, 'Username or password is incorrect')
  
  return render(request, 'accounts/login.html')


def logoutPage(request):
  logout(request)
  return redirect('login')


@unauthorized_user
def registerPage(request):
  form = CreateUserForm()
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')

      group = Group.objects.get(name='customer')
      user.groups.add(group)

      messages.success(request, 'An account for ' + username + ' was created')
      return redirect('login')
    
  context = {'form':form}
  return render(request, 'accounts/register.html', context)


def userPage(request):
  context = {}
  return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@admin_only
def dashboard(request):
  order_list = Order.objects.all()
  total_customers = Customer.objects.all().count()
  pending_orders = order_list.filter(status='pending').count()
  total_orders = order_list.count()
  myFilter = OrderFilter(request.GET, queryset=order_list)
  order_list = myFilter.qs

  context = {
    'pending_orders': pending_orders,
    'total_orders':total_orders,
    'total_customers': total_customers,
    'recent_orders':order_list,
    'myFilter':myFilter,
  }
  return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def totalOrders(request):
  total_orders = Order.objects.all()
  return render(request, 'accounts/total_orders.html', {'total_orders':total_orders})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
  customers = Customer.objects.all()
  customer_name = Customer.objects.get(id=pk)
  order = customer_name.order_set.all()

  context = {
    'customers':customers,
    'customer':customer_name,
    'orders':order,
  }
  return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request):
  customers = Customer.objects.all()
  return render(request, 'accounts/customers.html', {'customers':customers})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
  list = Product.objects.all()
  return render(request, 'accounts/products.html', {'product': list})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def status(request):
  orders = Order.objects.all()
  pending_status = Product.objects.filter(order__status='pending')
  in_transit = Product.objects.filter(order__status='Out for delivery')
  delivered = Product.objects.filter(order__status='delivered')

  context = {
    'pending_status':pending_status,
    'in_transit':in_transit,
    'delivered':delivered,
  }

  return render(request, 'accounts/status.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
  OrderFormSet = inlineformset_factory(Customer, Order, extra=2, fields=('product', 'status'))
  customer = get_object_or_404(Customer, id=pk)
  
  if request.method == 'POST':
    formset = OrderFormSet(request.POST, instance=customer, queryset=Order.objects.none())
    if formset.is_valid():
      formset.save()
      return redirect('/')
  else:
    formset = OrderFormSet(
      queryset=Order.objects.none(), 
      instance=customer,
    )
    
  return render(request, 'accounts/create_order.html', {'formset':formset})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
  order = Order.objects.get(id=pk)
  
  if request.method == 'POST':
    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
      form.save()
      return redirect('/')
  else:
    form = OrderForm(instance=order)
  return render(request, 'accounts/create_order.html', {'form':form})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
  order = Order.objects.get(id=pk)
  name = order.product

  if request.method == 'POST':
    order.delete()
    return redirect('/')
  
  return render(request, 'accounts/delete_order.html', {'item':name})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createCustomer(request):
  form = CustomerForm()
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('customers')
    
  return render(request, 'accounts/create_customer.html', {'form':form})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateCustomer(request, pk):
  customer = Customer.objects.get(id=pk)
  form = CustomerForm(instance=customer)
  if request.method == 'POST':
    form = CustomerForm(request.POST, instance=customer)