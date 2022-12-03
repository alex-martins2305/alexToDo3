from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasklist, name= 'tasklist'),
    path('newtask',views.newtask, name='newtask'),
    path('tasksvencidas', views.tasksvencidas, name= 'tasksvencidas'),
    path('tasksDoDia', views.tasksDoDia, name= 'tasksDoDia'),
    path('tasksFuturas', views.tasksFuturas, name= 'tasksFuturas'),
    path('tasksEncerradas', views.tasksEncerradas, name= 'tasksEncerradas'),
    path('tasksJustificadas', views.tasksJustificadas, name= 'tasksJustificadas'),
    path('task/<int:id>', views.taskview, name='taskview'),
    path('edit/starttask', views.starttask,name='starttask'),
    path('edit/justtask', views.justtask,name='justtask'),
    path('edit/stoptask', views.stoptask,name='stoptask'),
    path('edit/salvaObs', views.salvaObs,name='salvaObs'),
]