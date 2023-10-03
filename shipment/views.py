from django.shortcuts import render, redirect
import json
import requests


def new_order(request):
    return render(request, "order.html")
  