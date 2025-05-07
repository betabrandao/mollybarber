from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('cliente', 'Cliente'),
        ('barbeiro', 'Barbeiro'),
        ('admin', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='cliente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    class Meta:
        db_table = 'user_profile'

# Signal para criar UserProfile automaticamente após criar um User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='barber')
    available_hours = JSONField(default=dict)  # Ex.: {"segunda": ["09:00-18:00"]}
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Barbeiro)"

    class Meta:
        db_table = 'barbeiros'

class Category(models.Model):
    name = models.CharField(max_length=100)  # Ex.: "Cortes", "Estética"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categorias'

class Service(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='services')
    name = models.CharField(max_length=100)  # Ex.: "Corte de cabelo", "Barba"
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField()  # Ex.: timedelta(minutes=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.barber}"

    class Meta:
        db_table = 'servicos'

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    barber = models.ForeignKey(Barber, on_delete=models.RESTRICT, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, related_name='appointments')
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmado')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.client.get_full_name()} com {self.barber} ({self.appointment_datetime})"

    class Meta:
        db_table = 'agendamentos'
        unique_together = ('barber', 'appointment_datetime')  # Evita sobreposições