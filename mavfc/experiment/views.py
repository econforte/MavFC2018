from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import experimentsSerializer

from .models import *
from .forms import *

# Create your views here.

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def experimentJSON(request, pk):
    #getExperiment Implementation
    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ExperimentSerializer(experiment)
        return JSONResponse(serializer.data)
