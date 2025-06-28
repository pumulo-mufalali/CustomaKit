from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_user
from .models import Order, Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm, ProductForm
from django.forms import inlineformset_factory
from customer.models import Customer


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def totalOrders(request):
  total_orders = Order.objects.all()
  return render(request, 'product/total_orders.html', {'total_orders':total_orders})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
  list = Product.objects.all()


  return render(request, 'product/products.html', {'product': list})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def status(request):
  orders = Order.objects.all().count()
  intransit_orders = Order.objects.filter(status='Out for delivery')
  pending_orders = Order.objects.filter(status='pending')
  delivered_orders = Order.objects.filter(status='delivered')

  context = {
    'orders':orders,
    'intransit_orders':intransit_orders,
    'pending_orders':pending_orders,
    'delivered_orders':delivered_orders,
  }

  return render(request, 'product/status.html', context)


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
    
  return render(request, 'product/create_order.html', {'formset':formset})


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

  context = {
    'form':form,
  }
  return render(request, 'product/create_order.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
  order = Order.objects.get(id=pk)
  name = order.product

  if request.method == 'POST':
    order.delete()
    return redirect('/')
  
  return render(request, 'product/delete_order.html', {'item':name})

def deleteProduct(request, pk):
  product = Product.objects.get(id=pk)
  name = product.name

  if request.method == 'POST':
    product.delete()
    return redirect('product_list')
  
  return render(request, 'product/delete_order.html', {'item':name})

def createProduct(request):
  form = ProductForm()
  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('product_list')

  context = {'form':form}
  return render(request, 'product/create_product.html', context)