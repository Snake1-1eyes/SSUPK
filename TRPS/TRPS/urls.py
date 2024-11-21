"""
URL configuration for TRPS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app import views
urlpatterns = [
    path("", views.index, name='index'),
    path("sociodemographic", views.sociodemographic, name='sociodemographic'),
    path("general", views.general, name='general'),
    path("stationary_outpatient", views.stationary_outpatient, name='stationary_outpatient'),
    # path('graf3/', views.graf3, name='graf3'),
    path('admin/', admin.site.urls),
]
