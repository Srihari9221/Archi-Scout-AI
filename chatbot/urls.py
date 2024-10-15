from .import views
from django.urls import path

urlpatterns = [
    path("",views.chatbot,name="chat"),
    path("test/",views.test,name="test"),
    path('get-elevation-map/', views.elevation_map, name='elevation_map'),
    path('get-wind-map/', views.wind_map, name='wind_map'),
    path('get-disturbing-map/',views.disturbing_map,name='disturbing_map'),
    
]
