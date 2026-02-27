from django.urls import path
from . import views

urlpatterns = [
    path('employees', views.EmployeeListCreateView.as_view()),
    path('employees/<uuid:pk>', views.EmployeeDetailView.as_view()),
    path('attendance', views.AttendanceListCreateView.as_view()),
]
