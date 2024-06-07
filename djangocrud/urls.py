"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls), #URL para el sitio de administración de Django
    path('', views.home, name='home'), #URL para la página de inicio.
    path('signup/', views.signup, name='signup'), #URL para la página de registro.
    path('tasks/', views.tasks, name='tasks'),#URL para la lista de tareas pendientes
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),#URL para la lista de tareas completadas.
    path('tasks/create/', views.created_task, name='created_task'),#URL para la creación de nuevas tareas.
    path('logout/', views.signout, name='signout'),#URL para cerrar sesión.
    path('signin/', views.signin, name='signin'),#URL para iniciar sesión.
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),#URL para el detalle de una tarea específica.
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),#URL para marcar una tarea como completada
    path('tasks/<int:task_id>/delete', views.delete_task , name='delete_task'),#URL para eliminar una tarea.
    
]
