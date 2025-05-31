from django import forms
from .models import Service, Appointment, Category

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'name', 'duration', 'price']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': '00:30:00'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client_name','client_cell', 'service', 
                  'appointment_datetime', 'status']
        widgets = {
            'appointment_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']