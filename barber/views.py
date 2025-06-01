from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.template import loader
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils.dateparse import parse_datetime

from .decorators import barber_required
from .models import Barber, Category, Service, Appointment
from .forms import ServiceForm, AppointmentForm, CategoryForm

import json
from datetime import timedelta

def render2json(request, template, context):
    html = render_to_string(
        template_name=template, 
        context=context,
        request=request)
    return JsonResponse({'html': html})

# -------- AUTENTICACAO --------------
@login_required(login_url='login_user')
def show_home(request):
    available_hours = request.user.barber.available_hours
    context = {
        'available_hours': available_hours,
        'user': request.user,
    }
    return render(request, 'home.html', context)

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


# ---------- CATEGORIAS ----------- 
# TODO: avaliar se vai retornar só as categorias do barbeiro
# TODO: necessario alterar o models e adicionar o barber_id

@login_required
@barber_required
def list_categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render2json(request, 'categories.html', context)

@login_required
@barber_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('list_categories')
            return JsonResponse({'success': True})
    else:
        form = CategoryForm()
    return render2json(request, 'add_edit_category.html', {'form': form})

@login_required
@barber_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
            #return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render2json(request, 'add_edit_category.html', {'form': form, 'category': category})

@login_required
@barber_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return JsonResponse({'success': True})
        #return redirect('list_categories')
    return render2json(request, 'delete_category.html', {'category': category})


# ---------- SERVICOS ------------  

@login_required
@barber_required
def list_services(request):
    services = Service.objects.all()
    return render2json(request, 'services.html', {'services': services})

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
            return JsonResponse({'success': True})
            #return redirect('list_services')
    else:
        form = ServiceForm()
    
    return render2json(request, 'add_edit_service.html', {'form': form})

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
            return JsonResponse({'success': True})
            #return redirect('list_services')
    else:
        form = ServiceForm(instance=service)

    return render2json(request, 'add_edit_service.html', {'form': form})

@login_required
@barber_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.user.barber != service.barber:
        return HttpResponseForbidden("Você não pode excluir este serviço.")

    if request.method == 'POST':
        service.delete()
        return JsonResponse({'success': True})
        #return redirect('list_services')
    
    return render2json(request, 'delete_service.html', {'service': service})

# -------- AGENDAMENTO --------
@login_required
@barber_required

@login_required
@barber_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    context = {'appointment': appointment}
    return render2json(request, 'appointment_detail.html', context)

@login_required
@barber_required
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.barber = request.user.barber
            appointment.save()
            return JsonResponse({'success': True})
            #return redirect('list_appointments')
    else:
        form = AppointmentForm()
    return render2json(request, 'add_appointment.html', {'form': form})

@login_required
@barber_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = AppointmentForm(instance=appointment)
    return render2json(request, 'edit_appointment.html', {'form': form})

@login_required
@barber_required
def appointments_feed(request):
    start_date = parse_datetime(request.GET.get('start'))
    end_date = parse_datetime(request.GET.get('end'))
    appointments = Appointment.objects.filter(
        barber=request.user.barber,
        appointment_datetime__range=(start_date, end_date)
        ).order_by('appointment_datetime')

    eventos = []
    for agendamento in appointments:
        eventos.append({
            "id": agendamento.id,
            "title": f"{agendamento.service.name} - {agendamento.client_name}",
            "start": agendamento.appointment_datetime.isoformat(),
            "end": (agendamento.appointment_datetime + agendamento.service.duration).isoformat(),
            "url": reverse('appointment_details', args=[agendamento.id]),
            "classNames": agendamento.status,
        })

    return JsonResponse(eventos, safe=False)

# -------- HORARIOS DISPONIVEIS ------------- ok

@login_required
@barber_required
def barber_hours(request):
    barber = get_object_or_404(Barber, user_id=request.user.id)
    return render2json(request, 'barbers.html', {'barber': barber})

@login_required
@barber_required
def edit_barber_hours(request):
    barber = get_object_or_404(Barber, user_id=request.user.id)
    if request.method == 'POST':
        barber.available_hours = {
            'daysOfWeek': list(map(int, request.POST.getlist("days[]"))), 
            'startTime': request.POST['startTime'], 
            'endTime': request.POST['endTime']
            }
        barber.save()
        return JsonResponse({'success': True})
    
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
    return render2json(request, 'edit_barber_hours.html', context)
