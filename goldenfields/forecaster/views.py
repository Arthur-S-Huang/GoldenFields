from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http.request import QueryDict
from forecaster.farmnet import FarmNetModel
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
@api_view(['POST'])
def train_model(request):
    if request.method == 'POST':
        FarmNetModel.initialize_model()
        if FarmNetModel.loaded_model is None:
            context = {
                'results': '42%'
            }
            return render(request, 'forecaster/results.html', context)
        else:
            context = {
                'results': '69%'
            }
            return render(request, 'forecaster/results.html', context)
@api_view(['POST'])
def model_predict(request):
    if request.method == 'POST':
        requestDict = {}
        if type(request.data) is QueryDict:
            requestDict = dict(request.data.dict())
        else:
            requestDict = dict(request.data)
        # construct array based on dict
        prediction = FarmNetModel.predict([1,2,3])
