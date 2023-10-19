from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
import uuid

@login_required
def recipient_info(request):
    if request.method == 'POST':
        request.session['recipient_data'] = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'address': request.POST.get('address'),
        }
        return redirect('package')
    else:
        recipient_data = request.session.get('recipient_data', None)
        return render(request, 'recipient_info.html', {'recipient_data': recipient_data})

def package_info(request):
    if request.method == 'POST':
        request.session['package_data'] = {
            'package_name': request.POST.get('package_name'),
            'package_weight': request.POST.get('package_weight'),
            'package_description': request.POST.get('package_description'),
        }
        return redirect('confirm_order')
    else:
        package_data = request.session.get('package_data', None)
        return render(request, 'package.html')
    

@login_required
def confirm_order(request):
    recipient_data = request.session.get('recipient_data', {})
    package_data = request.session.get('package_data', {})

    if not recipient_data or not package_data:
        return redirect('order')  # Redirect to a suitable view

    if request.method == "POST":
        # Retrieve recipient and package data from the session
        recipient_data = request.session.get('recipient_data', {})
        package_data = request.session.get('package_data', {})

        # Create an instance of the combined model using the session data
        order = Order.objects.create(
            user=request.user,
            first_name=recipient_data.get('first_name', ''),
            last_name=recipient_data.get('last_name', ''),
            email=recipient_data.get('email', ''),
            phone_number=recipient_data.get('phone_number', ''),
            address=recipient_data.get('address', ''),
            package_name=package_data.get('package_name', ''),
            package_weight=package_data.get('package_weight', ''),
            package_description=package_data.get('package_description', ''),
            # tracking_number=str(uuid.uuid4())

        )
        print(order)

        # Redirect to the success page
        return redirect('order_success')

    return render(request, 'confirm_order.html', {
        'recipient_info': recipient_data,
        'package_info': package_data,
    })

@login_required
def submit_order(request):
        return redirect('order')  # Redirect to a suitable view if needed
    

def order_success(request):
    return render(request,'order_success.html')