"""MPM2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from account.apis import LoginAPI, ProfileAPI, ServiceListCreateAPI, ServiceRetrieveAPI

urlpatterns = [
    path('login/<int:phone>', LoginAPI.as_view()),
    path('verify/<int:phone>', LoginAPI.as_view()),
    path('profile/', ProfileAPI.as_view()),
    path('profile/<int:pk>', ProfileAPI.as_view()),
    path('services/', ServiceListCreateAPI.as_view()),
    path('service/<int:pk>', ServiceRetrieveAPI.as_view()),
]
