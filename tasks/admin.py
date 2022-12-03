from django.contrib import admin
from .models import Task

class ListandoTasks(admin.ModelAdmin):
    list_display =('id', 'titulo','etapas')
    list_display_links=('id', 'titulo')
    search_fields=('titulo',)
    list_per_page=10
    list_editable=('etapas',)

admin.site.register(Task, ListandoTasks)