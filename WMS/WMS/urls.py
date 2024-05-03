"""
URL configuration for WMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from main import views
from main.views import create_new_pallet_view, attach_pallet_to_cell_view, attach_product_to_pallet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('create_new_pallet/', create_new_pallet_view, name='create_new_pallet'),
    path('attach_pallet_to_cell/', attach_pallet_to_cell_view, name='attach_pallet_to_cell'),
    path('attach_product_to_pallet', attach_product_to_pallet, name='attach_product_to_pallet'),


    path('attach_pallet_to_cell/', attach_pallet_to_cell_view, name='attach_pallet_to_cell'),

    path('cells/', views.cell_list, name='cell_list'),
    path('cells/add/', views.add_cell, name='add_cell'),
    path('zones/', views.zone_list, name='zone_list'),
    path('zones/add/', views.add_zone, name='add_zone'),
    path('purchase', views.purchase_order_list, name='purchase_order_list'),


]
