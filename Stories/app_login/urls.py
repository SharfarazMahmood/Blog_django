from django.urls import path

from . import views

app_name = 'app_login'

urlpatterns  = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/', views.profile, name='profile'),
    path('user_profile_change/', views.user_profile_change, name='user_profile_change'),
    ### this is a built in form name
    path('password/', views.password_change, name='password_change'),
    path('add_profile_pic', views.add_profile_pic, name='add_profile_pic'),
    path('change_profile_pic', views.change_profile_pic, name='change_profile_pic'),
]
