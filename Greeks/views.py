from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from Greeks.models import Greeks
from Greeks.serializers import GreeksSerializer
from rest_framework.decorators import api_view
from Greeks.black_scholes import BlackScholes as bs

@api_view(['GET'])
def getGreeks(request):
    params = request.query_params
    try:
        greeks = bs.getOptionGreeks(
            params['option_type'],
            params['current_price'], 
            params['strike_price'],
            params['option_price'],
            params["current_date"],
            params["expiration_date"])
        return JsonResponse(greeks, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'error': "Bad request: required parameters are option_type, current_price, strike_price, option_price, current_date, expiration_date "},
         status=status.HTTP_400_BAD_REQUEST)
