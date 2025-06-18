from django.shortcuts import render, redirect
from .models import *
from .form import OrderForm, CustomerForm
 

def dashboard(request):
  order_list = Order.objects.all()
  total_customers = Customer.objects.all().count()
  pending_orders = order_list.filter(status='pending').count()
  total_orders = order_list.count()

  context = {
    'pending_orders': pending_orders,
    'total_orders':total_orders,
    'total_customers': total_customers,
    'recent_orders':order_list,
  }
  return render(request, 'accounts/dashboard.html', context)

def total_orders(request):
  total_orders = Order.objects.all()
  return render(request, 'accounts/total_orders.html', {'total_orders':total_orders})

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

def customers(request):
  customers = Customer.objects.all()
  return render(request, 'accounts/customers.html', {'customers':customers})


def products(request):
  list = Product.objects.all()
  return render(request, 'accounts/products.html', {'product': list})


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

def create_order(request):
  form = OrderForm()
  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/')
    
  return render(request, 'accounts/create_order.html', {'form':form})

def create_customer(request):
  form = CustomerForm()
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('customers')
    
  return render(request, 'accounts/create_customer.html', {'form':form})