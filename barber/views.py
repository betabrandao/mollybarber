from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import UserProfile, Barber, Category, Service, Appointment
from .forms import ServiceForm, AppointmentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

import json

@login_required(login_url='login/')
def show_home(request):
    template = loader.get_template('home.html')
    return render(request, 'home.html', {'user': request.user})

def barber_hours(request):
    barber = get_object_or_404(Barber, user_id=request.user.id)
    context = {'barber': barber}
    return render(request, 'barbers.json', context)

def list_categories(request):
    categories = Category.objects.all()
    template = loader.get_template('categories.html')
    context = {'categories': categories}
    return HttpResponse(template.render(context, request))

def list_services(request):
    services = Service.objects.all()
    template = loader.get_template('services.html')
    context = {'services': services}
    return HttpResponse(template.render(context, request))

def barber_services(request, barber_id):
    barber = get_object_or_404(Barber, pk=barber_id)
    services = barber.services.all()
    template = loader.get_template('barber_services.html')
    context = {'barber': barber, 'services': services}
    return HttpResponse(template.render(context, request))

def list_appointments(request):
    appointments = Appointment.objects.all()
    template = loader.get_template('appointments.html')
    context = {'appointments': appointments}
    return HttpResponse(template.render(context, request))

def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    template = loader.get_template('appointment_detail.html')
    context = {'appointment': appointment}
    return HttpResponse(template.render(context, request))

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    msg = ''
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
            msg = 'Credenciais inválidas'
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'msg': msg})

# - Funções do Forms
# -------- SERVIÇO --------
@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.barber = request.user.barber  # vincula ao barbeiro logado
            form.save()
            return redirect('list_services')
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})

def edit_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('list_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_service.html', {'form': form})

# -------- AGENDAMENTO --------
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('list_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form})

def barber_hours_list(request, barber_id):
    barber = get_object_or_404(Barber, id=barber_id)
    return render(request, 'barber_hours_list.html', {'barber': barber})


def edit_barber_hours(request):
    barber = get_object_or_404(Barber, user_id=request.user.id)
    if request.method == 'POST':
        barber.available_hours = {
            'daysOfWeek': list(map(int, request.POST.getlist("days[]"))), 
            'startTime': request.POST['startTime'], 
            'endTime': request.POST['endTime']
            }
        barber.save()
        return redirect('barber_hours')
    
    days = list(range(7))
    name = ['Domingo', 'Segunda', 'Terça', 
            'Quarta', 'Quinta', 'Sexta', 
            'Sábado']
    days_name = list(zip(days,name))
    context = {
        'barber': barber,
        'days': barber.available_hours.get('daysOfWeek'),
        'startTime':barber.available_hours.get('startTime'),
        'endTime': barber.available_hours.get('endTime'),
        'daysName': days_name,
        }
    return render(request, 'edit_barber_hours.html', context)