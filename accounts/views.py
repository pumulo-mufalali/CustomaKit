from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .filters import OrderFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .decorators import unauthorized_user, allowed_user, admin_only
from django.contrib import messages

from customer.models import Customer
from product.models import Order
from customer.forms import CustomerForm


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
      form.save()
      username = form.cleaned_data.get('username')

      messages.success(request, 'An account for ' + username + ' was created')
      return redirect('login')
    
  context = {'form':form}
  return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles='customer')
def settingsPage(request):
  customer = request.user.customer
  form = CustomerForm(instance=customer)

  if request.method == 'POST':
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    if form.is_valid():
      form.save()
      return redirect('settings')
  context = {'form':form}
  return render(request, 'accounts/account_settings.html', context)


def userPage(request):
  order = request.user.customer.order_set.all()

  # price += request.user.product.price
  total_orders = order.count
  intransit = order.filter(status='Intransit').count()
  delivered = order.filter(status='delivered').count()
  pending = order.filter(status='pending').count()
  
  context = {
    # 'price':price,
    'total_orders':total_orders,
    'intransit':intransit,
    'delivered':delivered,
    'pending':pending,
  }
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