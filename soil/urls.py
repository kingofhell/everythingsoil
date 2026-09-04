from django.urls import path
from . import views

app_name = 'soil'

urlpatterns = [
    path('', views.home, name='home'),
    path('soil/', views.soil_detail, name='soil_detail'),
    path('panja-bootham/', views.panja_bootham, name='panja_bootham'),
    path('panja-bootham/<slug:slug>/', views.element_detail, name='element_detail'),
    path('panja-bootha-lingeswarar/', views.lingeswarar, name='lingeswarar'),
    path('about/', views.about, name='about'),
]
