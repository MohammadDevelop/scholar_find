from rest_framework import serializers
from .models import Collegiate
from .models import Expertise


class CollegiateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collegiate
        fields = ('id', 'full_name')

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = ('id', 'title')