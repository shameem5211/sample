from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('edit_user/<int:user_id>/',views.edit_user,name='edit_user')
    
]