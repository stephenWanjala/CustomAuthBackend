from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/student/', views.student_registration, name='student_registration'),
    path('register/lecturer/', views.lecturer_registration, name='lecturer_registration'),
    path('home', views.home, name='home'),
]
