from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('usuario', 'usuario'),
        ('barbeiro', 'Barbeiro'),
        ('admin', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='usuario')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    class Meta:
        db_table = 'user_profile'

# Signal para criar UserProfile automaticamente após criar um User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Barber(models.Model):
    def default_available_hours():
        return {
            "daysOfWeek": [1,2,3,4,5],
            "startTime": "09:00",
            "endTime": "18:00"
            }
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='barber')
    available_hours = models.JSONField(default=default_available_hours,blank=True, null=True)  # Ex.: {"Category_name": ["08:00:00", "19:00:00"]}
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Barbeiro)"

    class Meta:
        db_table = 'barbeiros'

@receiver(post_save, sender=UserProfile)
def create_barber_if_needed(sender, instance, created, **kwargs):
    if instance.user_type == 'barbeiro':
        Barber.objects.get_or_create(user=instance.user)

class Category(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='categories')
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
    duration = models.DurationField()  # Ex.: timedelta(minutes=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - R$ {self.price}"


    class Meta:
        db_table = 'servicos'

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído'),
    ]
    client_name = models.CharField(max_length=50, blank=True, null=True)
    client_cell = models.CharField(max_length=15, blank=True, null=True)
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
