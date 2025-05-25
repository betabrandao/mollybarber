from django.urls import path
from .views import (
    BarberListCreateView, BarberDetailView,
    CategoryListCreateView, CategoryDetailView,
    ServiceListCreateView, ServiceDetailView,
    AppointmentListCreateView, AppointmentDetailView
)

urlpatterns = [
    path('barbers/', BarberListCreateView.as_view(), name='barber-list-create'),
    path('barbers/<int:pk>/', BarberDetailView.as_view(), name='barber-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
]
