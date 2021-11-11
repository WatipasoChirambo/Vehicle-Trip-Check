from django import http
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from home.models import Trip, Officer, TripInstance
from django.views import generic
from zone.settings import TIME_ZONE
from .models import *
from django.db.models import Q
from .forms import *
from django.core.paginator import EmptyPage, Paginator
from datetime import datetime, time, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import Registrationform
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from datetime import datetime,date
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.

def register(response):
    if response.method == "POST":
        form = Registrationform(response.POST)
        if form.is_valid():
            form.save()
        
        return redirect("index")
    else:
        form = Registrationform()
    return render(response, 'home/registration.html', {"form":form})

@login_required
def today(request):
    today = datetime.now().date()
    todays_trips = Trip.objects.filter(date_created=today)
    context = {
        "todays_trips":todays_trips,
        "today":today
    }
    return render(request, 'home/todays_trips.html', context)

@login_required
def yesterday(request):
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    yesterdays_trips = Trip.objects.filter(date_created=yesterday)
    context = {
        "yesterdays_trips":yesterdays_trips,
        "today":today
    }
    return render(request, 'home/yesterday_trips.html', context)

@login_required
def trips(request):
    today = date.today()
    search_trip = request.GET.get('search')
    if search_trip:
        car_reg = Trip.objects.filter(Q(car_reg_number__icontains=search_trip)|Q(driver__icontains=search_trip))
    else:
        car_reg = None
    all_users = get_user_model().objects.all()
    trips = Trip.objects.all()
    pages = Paginator(trips, 10)
    page = request.GET.get('page', 1)
    try:
        page = pages.page(page)
    except EmptyPage:
        page = pages.page(1)
    context = {
        "trips": page,
        'car_reg':car_reg,
        "today":today,
        "guys":all_users
    }
    return render(request, 'home/trips.html', context)

@login_required
def all_week(request):
    today = date.today()
    today = datetime.now().date()
    lasts = today - timedelta(7)

    last_weeks_trips = Trip.objects.filter(trip_date=lasts,trip_date__lte=today)
    context = {
        "last_weeks_trips":last_weeks_trips,
        "today":today
    }
    return render(request, 'home/trips.html', context)

@login_required
def trip(request, pk):
    try:
        trip = Trip.objects.get(id=pk)
    except Trip.DoesNotExist:
        Http404
    return render(request, 'home/trip.html', {"trip": trip})

@login_required
def update(request, pk):
    context ={}
    today = date.today()
    trip = get_object_or_404(Trip, id=pk)
    form = UpdateForm(request.POST or None, instance = trip)
    if form.is_valid():
        trip.time_in = datetime.now()
        form.save()
        return redirect('trips')
    context={"form":form,
             "trip":trip,
             "today":today
             }
    return render(request, "home/update.html", context)

@login_required
def index(request):
    trips = Trip.objects.all()
    form = TripsForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Checked In")
            form = TripsForm()
    context = {
        "trips": trips,
        "form": form,
        "today":today
    }
    return render(request, 'home/home.html', context)

def history(request):
    form = VehicleHistorySearchForm(request.POST or None)
    data = Trip.objects.filter(
        date_created__range=[
            form['start_date'].value(),
            form['end_date'].value()
        ]
    )
    context = {
        "trips": data,
        "form": form
    }
    return render(request, 'home/history.html', context)       
