from django.db import models
from django.contrib.auth.models import User #Modelo de usuario de Django.

#Task: Nombre de la clase que define el modelo de datos para una tarea.
#models.Model: La clase Task hereda de models.Model, lo que significa que es un modelo de Django y Django lo tratará como una tabla en la base de datos.
class Task(models.Model):
    title = models.CharField(max_length=100) #Define el campo título como un campo de texto de longitud máxima 
    description = models.TextField(blank=True) # Define el campo de texto para la descripción
    created = models.DateTimeField(auto_now_add=True) # Define el campo de fecha y hora para la creación
    datecompleted = models.DateTimeField(null=True, blank=True) # Define el campo de fecha y hora para la fecha completada
    important = models.BooleanField(default=False) # Define el campo booleano para la importancia
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Relación con el modelo 'User', indicando el propietario de la tarea.
    
    #Método __str__.
    #Método especial que define el comportamiento de impresión del objeto, devolviendo una cadena de texto que representa la tarea.
    def __str__(self):
        return self.title + '- by  ' + self.user.username