"""
URL configuration for signalLearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Home.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login, name='login'),
    path('signup/', Registration, name='registration'),
    # path('home/',Home, name='home'),
    path('home/',create_notification, name='home'),
    path('user-list/', UserList, name='user_list'),
    path('chat/<int:id>/', ChatView , name='chat'),
    # path('send-notification/<str:recipient_username>/', send_notification, name='send_notification'),
]
