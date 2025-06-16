
from django.urls import path
from .views  import hello,bye,edad,primer_plantilla,segunda_plantilla,tercer_plantilla,cuarta_plantilla,crear_musico,crear_album,first_api,serial_v1,person_list,person_detail,PersonAPIview,PersonAPIDetail,PersonMixinList,PersonMixinDetail,PersonList,PersonDetail


urlpatterns = [
    path('hello/',hello),
    path('bye/',bye),
    path('edad/<int:edad>/<int:futuro>',edad),
    path('plantilla1/',primer_plantilla),
    path('plantilla2/',segunda_plantilla),
    path('plantilla3/',tercer_plantilla),
    path('plantilla4/',cuarta_plantilla),
    path('crearmusico/<nombre>/<apellido>/<instrumento>',crear_musico),
    path('crearalbum/<nombre>/<int:estrellas>/<int:artista_id>',crear_album),
    path('api/first_api',first_api),
    path('api/serialv1',serial_v1),
    path('api/v1/person/',person_list),
    path('api/v1/person/<int:pk>/',person_detail),
    path('api/v2/person/',PersonAPIview.as_view()),
    path('api/v2/person/<int:pk>/',PersonAPIDetail.as_view()),
    path('api/v3/person/',PersonMixinList.as_view()),
    path('api/v3/person/<int:pk>/',PersonMixinDetail.as_view()),
    path('api/v4/person/',PersonList.as_view()),
    path('api/v4/person/<int:pk>/',PersonDetail.as_view()),
]