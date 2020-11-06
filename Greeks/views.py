from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from Greeks.models import Greeks
from Greeks.serializers import GreeksSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def getGreeks(request):
    params = request.query_params
    print(params)
    greeks = {'delta':1, 'gamma':2, 'theta':3, 'vega':4}
    greeksSerializer = GreeksSerializer(greeks)
    return JsonResponse(greeksSerializer.data, status=status.HTTP_201_CREATED)