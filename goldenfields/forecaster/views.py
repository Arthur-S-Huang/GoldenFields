from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http.request import QueryDict


# Create your views here.
def index(request):
    context = {
        'current_location': 'URBANAVILLE',
        'current_temp': '109 degrees F'
    }
    return render(request, 'forecaster/index.html', context)


@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        context = {
            'results': '42%'
        }
        return render(request, 'forecaster/results.html', context)
