from rest_framework import serializers 
from Greeks.models import Greeks
 
class GreeksSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Greeks
        fields = ('delta',
                  'gamma',
                  'theta',
                  'vega')