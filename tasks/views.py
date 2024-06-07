from django.shortcuts import render, redirect, get_object_or_404 #render combina una plantilla con datos y devuelve un objeto HttpResponse y redirect redirige a una URL específica.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #UserCreationForm crea un formulario de creación de usuario, AuthenticationForm crea un formulario de autenticación.
from django.contrib.auth.models import User #Modelo de usuario de Django.
from django.contrib.auth import login, logout, authenticate #login es una función para autenticar a un usuario y logout es una función para cerrar la sesión de un usuario. authenticate es una función para autenticar a un usuario.
from django.db import IntegrityError #Excepción que se lanza cuando se viola una restricción de integridad. 
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required 



#El propósito de esta vista es redirigir a la página de inicio. su lógica
#simplemente devuelve a la plantilla home.html.
def home(request):
   return render(request, 'home.html')

#Maneja el registro de nuevos usuarios.
#request: Parámetro que representa la solicitud HTTP realizada por el usuario. Este objeto contiene toda la información sobre la solicitud que el navegador del usuario ha hecho al servidor.
def signup(request):

    #Si la solicitud es GET, renderiza la plantilla signup.html con el formulario de creación de usuario.
    if request.method == 'GET': #Compara el método de la solicitud con la cadena 'GET'. Si es GET, significa que el usuario está solicitando ver la página (por ejemplo, navegando a la URL).
        return render(request, 'signup.html',{
            'form': UserCreationForm #Es un formulario estándar de Django para crear un nuevo usuario.
        })
    #Si la solicitud no es GET, se asume que es POST. ,Si la solicitud es POST, compara las contraseñas y crea un nuevo usuario si las contraseñas coinciden    
    else:
        
        #request.POST: Diccionario que contiene todos los datos enviados en la solicitud POST. Permite acceder a los datos enviados desde el formulario.
        if request.POST['password1'] == request.POST['password2']:
            
            #Intenta ejecutar el bloque de código para crear un nuevo usuario
            try:
                
                #Crea un nuevo usuario con el nombre de usuario y la contraseña proporcionados
                user=User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                
                #Inicia sesión automáticamente con el nuevo usuario.
                #login: Función de Django que maneja el inicio de sesión del usuario.
                login(request, user)
                #Redirecciona a la página de tareas si el usuario se crea correctamente.
                return redirect('tasks')
            # Si ocurre un error(Usuario ya existente), muestra un error 
            except IntegrityError:
                return render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': 'Usuario already exists'
            })
        # Si las contraseñas no coinciden, muestra un error
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error': 'Contraseñas no coinciden'
        })


#@login_required: Es un decorador proporcionado por Django que se asegura de que el usuario esté autenticado antes de permitir el acceso a la vista.
#Evita que usuarios no autenticados accedan a la vista tasks. Si un usuario no autenticado intenta acceder a esta vista, será redirigido a la página de inicio de sesión.
@login_required                        
# Renderiza la plantilla tasks.html.
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)#realiza una consulta a la base de datos para obtener todas las tareas que cumplen con los siguientes criterios
    return render(request, 'tasks.html', {'tasks': tasks}) 



#Muestra las tareas completadas del usuario autenticado.
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')#Esta linea realiza una consulta a la base de datos para obtener todas las tareas
    #con los siguientes criterios.
    #Usuario Autenticado: Solo selecciona las tareas que pertenecen al usuario que ha iniciado sesión en la aplicación (request.user).
    #Tareas Completadas: Solo selecciona las tareas que tienen una fecha de completado (datecompleted no es nulo).
    #Orden Descendente: Ordena las tareas por la fecha de completado en orden descendente (de más reciente a más antigua).
    #El resultado de esta consulta se almacena en la variable tasks. Esto permite que la aplicación maneje y muestre solo las tareas completadas del usuario autenticado.
    return render(request, 'tasks.html', {'tasks': tasks, 'completed': True})


# Maneja el cierre de sesión del usuario.
@login_required                        
def signout(request):
    logout(request)#Función de Django que maneja el cierre de sesión del usuario.
    return redirect('home')#Redirige al usuario a la página de inicio después de cerrar la sesión.


# Se maneja el inicio de sesión del usuario.
def signin(request):
    #Si la solicitud es GET, renderiza la plantilla signin.html con el formulario de autenticación.
    if request.method == 'GET':
        
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    #Auntentica al usuario con el nombre de usuario y la contraseña.    
    else:
        #Autentica al usuario con las credenciales proporcionadas.
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        #Si la autenticación falla, muestra un error.
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        #Si la autenticación es exitosa, redirecciona a la página de tareas.
        else:
            login(request, user)
            return redirect('tasks')
        
        
#Maneja la creación de nuevas tareas.
@login_required                                
def created_task(request):
    
    #Verifica si el método de la solicitud es HTTP es GET
    #request: Objeto que representa la solicitud HTTP realizada por el usuario
    #GET: Método de solicitud utilizado para solicitar datos desde un servidor.
    
    #Si la solicitud es GET, renderiza la plantilla created_task.html con un formulario de tarea (TaskForm).
    if request.method == 'GET':
        return render(request, 'created_task.html', {
            'form': TaskForm   
        })
    
    #Si la solicitud no es GET (asumimos que es POST).
    #POST: Método de solicitud utilizado para enviar datos al servidor
    
    else:
        try:
            form = TaskForm(request.POST)
            
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            
            #Vuelve a renderizar la plantilla created_task.html con el formulario de tarea (TaskForm).
            return redirect('tasks')
        except ValueError:
            return render(request, 'created_task.html', {
                'form': TaskForm,   
                'error': 'Porfavor provee dato valido'
            })

#Muestra y permite editar el detalle de una tarea específica.
@login_required                            
def task_detail(request,task_id):
    if request.method == 'GET':#Verifica si el método de la solicitud HTTP es GET. Esto indica que el usuario está solicitando ver la página de detalles de la tarea.
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)#Crea una instancia del formulario TaskForm con los datos de la tarea recuperada.
        return render(request, 'task_detail.html', {'task': task, 'form': form})#Función de Django que combina una plantilla con un contexto de datos y devuelve un objeto HttpResponse con el contenido renderizado.
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)#Obtiene la tarea específica del usuario autenticado o devuelve un error 404 si no se encuentra.
            form = TaskForm(request.POST, instance=task)#Crea una instancia del formulario TaskForm con los datos enviados en la solicitud POST y la tarea existente.
            form.save()#Guarda los datos del formulario en la base de datos, actualizando la tarea existente.
            return redirect('tasks')#Función de Django que redirige a una URL específica. Redirige al usuario a la página de tareas después de actualizar la tarea.
        except ValueError:
            
            #Función de Django que combina una plantilla con un contexto de datos y devuelve un objeto HttpResponse con el contenido renderizado, incluyendo un mensaje de error.
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Por favor provee dato valido'})
        


#Marca una tarea como completada. 
@login_required                            
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)#Esta línea obtiene la tarea específica del usuario autenticado o devuelve un error 404 si no se encuentra.
    if request.method == 'POST':#Verifica si el método de la solicitud HTTP es POST. Esto asegura que la tarea solo se marque como completada cuando se envíe un formulario POST.
        task.datecompleted = timezone.now()#Establece el campo datecompleted de la tarea a la fecha y hora actuales.
        task.save()#Guarda el objeto task actualizado en la base de datos.
        return redirect('tasks')
    

#Elimina una tarea. 
@login_required                            
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)#Esta línea obtiene la tarea específica del usuario autenticado o devuelve un error 404 si no se encuentra.
    if request.method == 'POST':#Verifica si el método de la solicitud HTTP es POST. Esto asegura que la tarea solo se elimine cuando se envíe un formulario POST
        task.delete()#Eliminar la tarea específica del usuario autenticado.
        return redirect('tasks')#Redirige al usuario a la página de tareas después de eliminar la tarea.
    
    
             
               
        
    
            
    
 
            
            

        
        




        
         

                


   
