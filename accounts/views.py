from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .form import OrderForm, CustomerForm
from django.forms import inlineformset_factory
 

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

def totalOrders(request):
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

def deleteOrder(request, pk):
  order = Order.objects.get(id=pk)
  name = order.product

  if request.method == 'POST':
    order.delete()
    return redirect('/')
  
  return render(request, 'accounts/delete_order.html', {'item':name})

def createCustomer(request):
  form = CustomerForm()
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('customers')
    
  return render(request, 'accounts/create_customer.html', {'form':form})

def updateCustomer(request, pk):
  customer = Customer.objects.get(id=pk)
  form = CustomerForm(instance=customer)
  if request.method == 'POST':
    form = CustomerForm(request.POST, instance=customer)
