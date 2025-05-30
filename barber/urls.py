from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home, name='home'),
    path('barbeiros/', views.list_barbers, name='list_barbers'),
    path('categorias/', views.list_categories, name='list_categories'),
    path('servicos/', views.list_services, name='list_services'),
    path('barbeiro/<int:barber_id>/servicos/', views.barber_services, name='barber_services'),
    path('agendamentos/', views.list_appointments, name='list_appointments'),
    path('agendamento/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    path('registrar/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),

    # Serviços
    path('servicos/adicionar/', views.add_service, name='add_service'),
    path('servicos/<int:service_id>/editar/', views.edit_service, name='edit_service'),

    # Agendamentos
    path('agendamentos/adicionar/', views.add_appointment, name='add_appointment'),
    path('agendamentos/<int:appointment_id>/editar/', views.edit_appointment, name='edit_appointment'),

    path('barbeiro/<int:barber_id>/horarios/', views.barber_hours_list, name='list_barber_hours'),
    path('barbeiro/<int:barber_id>/horarios/adicionar/', views.add_barber_hours, name='add_barber_hours'),
    path('barbeiro/<int:barber_id>/horarios/<int:index>/editar/', views.edit_barber_hours, name='edit_barber_hours'),
    path('barbeiro/<int:barber_id>/horarios/<int:index>/excluir/', views.delete_barber_hours, name='delete_barber_hours'),

]
