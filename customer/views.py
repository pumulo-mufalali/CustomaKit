from django.shortcuts import render, redirect
from accounts.decorators import allowed_user
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer
from product.models import Order

# @login_required(login_url='login')
# @allowed_user(allowed_roles=['admin'])
# def updateCustomer(request, pk):
#   customer = Customer.objects.get(id=pk)
#   form = CustomerForm(instance=customer)
#   if request.method == 'POST':
#     form = CustomerForm(request.POST, instance=customer)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request):
  customers = Customer.objects.all()
  return render(request, 'customer/customers.html', {'customers':customers})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
  customers = Customer.objects.all()
  customer_name = Customer.objects.get(id=pk)
  order = customer_name.order_set.all()

  total_order=0.0
  orders = Order.objects.filter(customer_id=pk)

  for item in orders:
    total_order += item.product.price

  context = {
    'customers':customers,
    'total_order':total_order,
    'customer':customer_name,
    'orders':order,
  }
  return render(request, 'customer/customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createCustomer(request):
  form = CustomerForm()
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('customer/customers')
    
  context = {
    'form':form,
  }
    
  return render(request, 'customer/create_customer.html', context)