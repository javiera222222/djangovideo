#from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render
from .models import Musician,Album,Person
from .serializer import PersonaSerializer
from .serializer import PersonSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import mixins
from rest_framework import generics
def hello(request):
    return HttpResponse("hola mundo")

def bye(request):
    return HttpResponse("chau mundo")


def edad(request,edad,futuro):
    incremento= futuro -date.today().year
    cumplira=edad + incremento
    return HttpResponse("En el año %d cumpliras %d"%(futuro,cumplira))


def primer_plantilla(request):
    plantilla="""
    <html> 
    <body>
    <h2> {{variable}} esta es mi primer plantilla</h2>
    </body>
    </html>
    """
    template=Template(plantilla)
    ctx=Context({'variable':'hola'})
    mensaje=template.render(ctx)
    return HttpResponse(mensaje)

#mejor organizacion, esta llama a una plantilla aparte
def segunda_plantilla(request):
   
    template=get_template("segunda_plantilla.html")
    mensaje=template.render({'variable':'hola','fecha_actual':date.today})
    return HttpResponse(mensaje)

def tercer_plantilla(request):
    return render(request,"tercer_plantilla.html",{'variable':'hola','fecha_actual':date.today})


class Persona(object):
    def __init__(self,nombre,apellido):
        self.nombre =nombre
        self.apellido =apellido

def cuarta_plantilla(request):
    persona =Persona("Javiera","Guzman")

    arreglo=[1,2,3,4,5]

    return render(request,"cuarta_plantilla.html",{'nombre':persona.nombre,'apellido':persona,'fecha_actual':date.today,'variable_arreglo':arreglo})

#ejemplo para usar los modelos y hacer una vista de los datos de la base de datos
def crear_musico(request,nombre,apellido,instrumento):
    per=Musician(first_name=nombre, last_name=apellido, instrument=instrumento)
    per.save()
    mensaje="se creo el musico %s %s con id %d"%(per.first_name,per.last_name,per.id)
    return HttpResponse(mensaje)

def crear_album(request,nombre,estrellas,artista_id):
    art=Musician.objects.get(id=artista_id)
    album=Album(name=nombre,release_date=date.today(), num_stars=estrellas,artist=art)
    album.save()
    mensaje="se creo el album %s del artista %s con id %d"%(album.name,art.last_name,album.id)
    return HttpResponse(mensaje)

@csrf_exempt
def first_api(request):
   if request.method== 'GET':
        respuesta = {
            
        }
        return JsonResponse(respuesta)
   elif request.method== 'POST':
        datos = json.loads(request.body)
        nombre=datos['nombre']
        apellido=datos['apellido']
        edad=datos['edad']
        respuesta= {
            'nombre2':nombre,
            'apellido2':apellido,
            'edad2':edad
        }
        return JsonResponse(respuesta)
   return None      

@csrf_exempt
def serial_v1(request):
   
   if request.method== 'POST':
        datos = json.loads(request.body)
        serializador= PersonaSerializer(data=datos)
        if serializador.is_valid():
            return JsonResponse(serializador.validated_data, status=201)
        else:
            return JsonResponse(serializador.errors, status=400)
       
   return None      

@csrf_exempt
def person_list(request):
   if request.method == 'GET':
        personas = Person.objects.all()
        serializer = PersonSerializer(personas, many=True).data
        return JsonResponse(serializer, safe=False)
   

   if request.method== 'POST':
        datos = json.loads(request.body)
        serializer= PersonSerializer(data=datos)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.validated_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
       
   return None      


@csrf_exempt
def person_detail(request,pk):
   if request.method == 'GET':
        persona = Person.objects.get(pk=pk)
        serializer = PersonSerializer(persona).data
        return JsonResponse(serializer, safe=False)
   

   if request.method== 'PUT':
        datos = json.loads(request.body)
        persona = Person.objects.get(pk=pk)
        serializer= PersonSerializer(persona,data=datos)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.validated_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


   if request.method== 'DELETE':
      
        persona = Person.objects.get(pk=pk)
        persona.delete()
        return HttpResponse(status=204)
       
   return None      



class PersonAPIview(APIView):

    def get(self, request, format=None):
        personas = Person.objects.all()
        serializer = PersonSerializer(personas, many=True).data
        return JsonResponse(serializer, safe=False)
    
    def post(self, request, format=None):
        datos = json.loads(request.body)
        serializer= PersonSerializer(data=datos)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PersonAPIDetail(APIView):
    def get_object(self,pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404
        
    def get(self,request, pk, format=None):
        person =self.get_object(pk)
        serializer =PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, dormat=None):
        person= self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
           

class PersonMixinList( mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset =Person.objects.all()
    serializer_class = PersonSerializer     

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class PersonMixinDetail( mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset =Person.objects.all()
    serializer_class = PersonSerializer     

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        


class PersonList(generics.ListCreateAPIView):
    queryset =Person.objects.all()
    serializer_class = PersonSerializer  

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Person.objects.all()
    serializer_class=PersonSerializer           