from django.urls import path

from forecaster import views

app_name = 'forecaster'

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
]