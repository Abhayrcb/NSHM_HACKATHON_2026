from django.urls import path
from .views import RegisterUserView,DashboardView,LoginView

urlpatterns = [
    path("register/",RegisterUserView.as_view(),name='register'),
    path("dashboard/",DashboardView.as_view()),
    path('login/',LoginView.as_view()),
    
]

