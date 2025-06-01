from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.show_home, name='home'),
    path('registrar/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', LogoutView.as_view(next_page='login_user'), name='logout'),

    # reset de senha
    path('senha/esqueci/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
        ), name='password_reset'),

    path('senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
        ), name='password_reset_done'),

    path('senha/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
        ), name='password_reset_confirm'),

    path('senha/completa/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
        ), name='password_reset_complete'),

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
    path('agendamento/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    path('agendamentos/adicionar/', views.add_appointment, name='add_appointment'),
    path('agendamentos/<int:appointment_id>/editar/', views.edit_appointment, name='edit_appointment'),
    path('api/agendamentos/', views.appointments_feed, name='appointments_feed'),

    # Horario de trabalho - ok
    path('horarios/', views.barber_hours, name='barber_hours'),
    path('horarios/editar/', views.edit_barber_hours, name='edit_barber_hours'),

]
