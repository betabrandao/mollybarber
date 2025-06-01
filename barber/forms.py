from django import forms
from .models import Service, Appointment, Category

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'name', 'duration', 'price']
        labels = {
            'category': 'Categoria', 
            'name': 'Nome do Serviço',
            'duration': 'Duração', 
            'price': 'Preço R$'
        }
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': '00:30:00'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client_name','client_cell', 'service', 
                  'appointment_datetime', 'status']
        labels = {
            'client_name': 'Nome do Cliente',
            'client_cell': 'Celular do Cliente', 
            'service': 'Serviço Prestado', 
            'appointment_datetime': 'Data e Hora da agenda', 
            'status': 'Status do Serviço'
        }
        widgets = {
            'appointment_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Nome'
        }