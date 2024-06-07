#Se define un formulario basado en el modelo Task

from django import forms #Importa el módulo forms de Django, que proporciona las clases y funciones necesarias para definir formularios.
from .models import Task#Importa el modelo Task desde el archivo models.py en el mismo directorio. Esto permite usar el modelo Task en la definición del formulario.

#Crear un formulario basado en el modelo Task y especifica los campos del modelo que se incluirán en el formulario.
class TaskForm(forms.ModelForm):
    #Define la configuración del formulario
    class Meta:#Clase anidada dentro de TaskForm que define la configuración del formulario.
        #Especifica que el formulario se basa en el modelo Task.
        model = Task
        #Especifica los campos del modelo que se incluirán en el formulario.
        fields = ['title', 'description', 'important']
        
        widgets = { #Especifica los widgets personalizados para cada campo del formulario.
            'title': forms.TimeInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center'}),
        }