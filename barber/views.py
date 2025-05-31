from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

from .decorators import barber_required
from .models import Barber, Category, Service, Appointment
from .forms import ServiceForm, AppointmentForm, CategoryForm

import json

@login_required(login_url='login_user')
def show_home(request):
    template = loader.get_template('home.html')
    return render(request, 'home.html', {'user': request.user})

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


# ---------- CATEGORIAS ----------- ok

@login_required
@barber_required
def list_categories(request):
    categories = Category.objects.all()
    template = loader.get_template('categories.html')
    context = {'categories': categories}
    return HttpResponse(template.render(context, request))

@login_required
@barber_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'add_edit_category.html', {'form': form})

@login_required
@barber_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'add_edit_category.html', {'form': form, 'category': category})

@login_required
@barber_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('list_categories')
    return render(request, 'delete_category.html', {'category': category})


# ---------- SERVICOS ------------ ok
@login_required
@barber_required
def list_services(request):
    services = Service.objects.all()
    template = loader.get_template('services.html')
    context = {'services': services}
    return HttpResponse(template.render(context, request))

@login_required
@barber_required
def add_service(request):
    if not hasattr(request.user, 'barber'):
        return HttpResponseForbidden("Apenas barbeiros podem cadastrar serviços.")
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.barber = request.user.barber
            service.save()
            return redirect('list_services')
    else:
        form = ServiceForm()
    
    return render(request, 'add_edit_service.html', {'form': form})

@login_required
@barber_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.user.barber != service.barber:
        return HttpResponseForbidden("Você não pode editar este serviço.")

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('list_services')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'add_edit_service.html', {'form': form})

@login_required
@barber_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.user.barber != service.barber:
        return HttpResponseForbidden("Você não pode excluir este serviço.")

    if request.method == 'POST':
        service.delete()
        return redirect('list_services')
    
    return render(request, 'delete_service.html', {'service': service})

# -------- AGENDAMENTO --------
@login_required
@barber_required
def list_appointments(request):
    appointments = Appointment.objects.filter(barber=request.user.barber).order_by('appointment_datetime')
    template = loader.get_template('appointments.html')
    context = {'appointments': appointments}
    return HttpResponse(template.render(context, request))

@login_required
@barber_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    template = loader.get_template('appointment_detail.html')
    context = {'appointment': appointment}
    return HttpResponse(template.render(context, request))

@login_required
@barber_required
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.barber = request.user.barber
            appointment.save()
            return redirect('list_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})

@login_required
@barber_required
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

# -------- HORARIOS DISPONIVEIS ------------- ok

@login_required
@barber_required
def barber_hours(request):
    barber = get_object_or_404(Barber, user_id=request.user.id)
    context = {'barber': barber}
    return render(request, 'barbers.json', context)

@login_required
@barber_required
def edit_barber_hours(request):
    barber = get_object_or_404(Barber, user_id=request.user.id)
    if request.method == 'POST':
        barber.available_hours = {
            'daysOfWeek': (map(int, request.POST.getlist("days[]"))), 
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