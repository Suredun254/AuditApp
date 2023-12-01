from django.urls import path,re_path
from . import views
from django.contrib.auth import views as auth_views

#define app name
app_name='accounts'

#create url patterns
urlpatterns = [
    path('',views.login, name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]