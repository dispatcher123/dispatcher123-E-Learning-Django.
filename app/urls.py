from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('premium/',premium,name='premium'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('category/<slug:slug>/',category,name='category'),
    path('course-detail/<slug:slug>/',course_detail,name='course_detail'),
    path('userpage/',userpage,name='userpage'),
    path('charge/',charge,name='charge')
]
