from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

    def validate_nisit(self, value):
        if Person.objects.filter(nisit=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("รหัสนิสิตนี้มีอยู่แล้ว")
        return value