from models import License
from rest_framework import serializers

class License_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = License
        fields = []