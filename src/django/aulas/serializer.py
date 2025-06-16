from rest_framework import serializers
from .models import Person

class PersonaSerializer(serializers.Serializer):
    nombre= serializers.CharField(max_length=100)
    apellido= serializers.CharField(max_length=100)
    edad= serializers.IntegerField()


          
    def validate_edad(self, value):
       if value < 18:
           raise serializers.ValidationError('edad insuficiente')
       return value
    
    def validate_nombre(self, value):
        correcciones ={
            'hariel': 'ariel'
        }
        nombre_normalizado= value.strip().lower()
        return correcciones.get(nombre_normalizado, value.strip()).capitalize()
    
    def validate_apellido(self, value):
        return value.strip().capitalize()


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        #fields = ('age','first_name') solo serializa ese campo