from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
import requests

@login_required
def order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        
        # Process the data as needed (e.g., save to the database)
        
        # Redirect to the package_info view
        return redirect('package_info')
        
    return render(request, "order.html")

def package_info(request):
    return render(request, "package.html")
