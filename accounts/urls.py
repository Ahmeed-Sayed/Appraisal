from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('create-user/', views.CreateUser.as_view(), name="create-user")
]
