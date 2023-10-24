from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShipmentForm
from django.http import HttpResponse
from .models import Shipment
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


def create_new_shipment(request):
    if request.method == 'POST': # create shipment
        form = ShipmentForm(request.POST)
        if form.is_valid():
            new = form.save()
            data = {'message': 'new order created'}
            data = json.dumps(data)
            return HttpResponse(data, content_type = 'application/json')

    if request.method == 'GET': #view shipment
        if request.user.is_authenticated:
            user = request.user
            orders = Shipment.objects.filter(customer_id=user.id, is_active = True)
            form = ShipmentForm()
            return render(request, 'test.html', {'orders': orders, 'form': form})
        else:
            data = {
                'response': 'Please Login to access this'
            }
            data = json.dumps(data)
            return HttpResponse(data, content_type = 'application/json')


def cancel_shipment(request, id):# cancel shipment
    order = Shipment.objects.get(order_id = id)
    order.is_active = False
    order.save()

    data = {
        'response': 'Order Cancelled'
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type = 'application/json')

def inactivate_shipments(request):# render inactive shipment
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            orders = Shipment.objects.filter(customer_id=user.id, is_active = False)
            return render(request, 'test.html', {'orders': orders})
        else:
            data = {
                'response': 'Please Login to access this'
            }
            data = json.dumps(data)
            return HttpResponse(data, content_type = 'application/json')

def activate_cancelled_shipment(request,id):# activate cancelled shipments
    order = Shipment.objects.get(order_id = id)
    order.is_active = True
    order.save()

    data = {
        'response': 'Order Activated'
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type = 'application/json')

def update_shipment(request, id):# update shipment
    obj = get_object_or_404(Shipment, order_id = id)

    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ShipmentForm(instance=obj)

    return render(request, 'test.html', {'form': form})

def track_shipment(request, id):# track shipment
    pass
def package_info(request):
    return render(request, "package.html")
