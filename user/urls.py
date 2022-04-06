from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('home', views.home, name='home'),
    # path('account/', views.account, name='account'),
]
