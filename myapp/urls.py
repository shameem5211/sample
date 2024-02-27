from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('home',views.home,name='home'),
    path('user_logout',views.user_logout,name='user_logout')
]