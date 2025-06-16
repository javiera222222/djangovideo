# CONTRUCCION DE LA IMAGEN

# que imagen vamos a usar y que version,desde donde la empezamos a crear 
FROM python:3.12-bookworm
# corro comandos con RUN, lo axctualizamos
RUN apt-get update && apt-get install python3-dev libgdal-dev graphviz graphviz-dev -y --force-yes
# defino directorio  donde vamos a aestar cuando arranque la imagen
WORKDIR /usr/src/app

# actualizamos el comando pip
RUN pip install --upgrade pip && pip install --upgrade setuptools
# copio el archivo requirements para mandarlo desde la pc al directorio dentro de la imagen
COPY requirements.txt ./
#corro los comandos escritos en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# expongo el puerto
EXPOSE 8000
# inicio el proyecto django
# creo proyecto que no existe, corro comando sjando-admin staproyect nombre:app y nombre de carpeta: . (porque estamos dentro)



# comando para levantar la imagen y que quede corriendo docker
CMD ["python","manage.py","runserver","0.0.0.0:8000"]