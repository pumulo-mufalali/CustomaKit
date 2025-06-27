from django.shortcuts import render, redirect
from accounts.decorators import allowed_user
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateCustomer(request, pk):
  customer = Customer.objects.get(id=pk)
  form = CustomerForm(instance=customer)
  if request.method == 'POST':
    form = CustomerForm(request.POST, instance=customer)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request):
  customers = Customer.objects.all()
  return render(request, 'accounts/customers.html', {'customers':customers})


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
def createCustomer(request):
  form = CustomerForm()
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('customers')
    
  return render(request, 'accounts/create_customer.html', {'form':form})