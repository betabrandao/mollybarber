from django import forms
from .models import Service, Appointment

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'name', 'description', 'duration', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'duration': forms.TextInput(attrs={'placeholder': '00:30:00'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'appointment_datetime', 'status']
        widgets = {
            'appointment_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
