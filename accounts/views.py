from django.shortcuts import render

def dashboard(request):
  return render(request, 'accounts/dashboard.html')

def customer(request):
  return render(request, 'accounts/customer.html')

def products(request):
  return render(request, 'accounts/products.html')

def status(request):
  return render(request, 'accounts/status.html')