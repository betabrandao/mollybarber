from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home, name='home'),
    path('registrar/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),

    # Categorias -ok
    path('categorias/', views.list_categories, name='list_categories'),
    path('categorias/adicionar/', views.add_category, name='add_category'),
    path('categorias/<int:category_id>/editar/', views.edit_category, name='edit_category'),
    path('categorias/<int:category_id>/excluir/', views.delete_category, name='delete_category'),


    # Serviços - ok
    path('servicos/', views.list_services, name='list_services'),
    path('servicos/adicionar/', views.add_service, name='add_service'),
    path('servicos/<int:service_id>/editar/', views.edit_service, name='edit_service'),
    path('servicos/<int:service_id>/excluir/', views.delete_service, name='delete_service'),

    # Agendamentos - ok
    path('agendamentos/', views.list_appointments, name='list_appointments'),
    path('agendamento/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    path('agendamentos/adicionar/', views.add_appointment, name='add_appointment'),
    path('agendamentos/<int:appointment_id>/editar/', views.edit_appointment, name='edit_appointment'),

    # Horario de trabalho - ok
    path('horarios/', views.barber_hours, name='barber_hours'),
    path('horarios/editar/', views.edit_barber_hours, name='edit_barber_hours'),

]
