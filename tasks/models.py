from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    STATUS=(
        ("ativa", "ativa"),
        ("rascunho", "rascunho"),
        ("suspensa", "suspensa"),
    )
    TEMPO=(
        ('não iniciada', 'não iniciada'),
        ('iniciada','iniciada'),
        ('finalizada', 'finalizada'),
        ('justificada','justificada'),
        ('atrasada','atrasada'),
    )
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo=models.CharField(max_length=255)
    descricao=models.TextField()
    status=models.CharField(
        max_length=13,
        choices=STATUS, 
        )
    etapas=models.CharField(
        max_length=13,
        choices=TEMPO, 
        )
    created_at=models.DateField(auto_now_add=True)
    start_at=models.DateField(auto_now=True)
    ends_at=models.DateField(default='9999-01-01')
    update_at=models.DateField(auto_now=True)
    obs=models.TextField(blank=True)
    concluida=models.BooleanField(default=False)
    concluida_at=models.DateField(blank=True)
    adiada=models.BooleanField(default=False)

    def __str__(self):
        return self.titulo