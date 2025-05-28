from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import UserProfile, Barber, Category, Service, Appointment
from .forms import ServiceForm, AppointmentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

def show_home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))

def list_barbers(request):
    barbers = Barber.objects.all()
    template = loader.get_template('barbers.html')
    context = {'barbers': barbers}
    return HttpResponse(template.render(context, request))

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
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
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