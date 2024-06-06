from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='почта', unique=True)
    name = models.CharField(max_length=150, verbose_name='Ф.И.О', **NULLABLE)
    comment = models.CharField(max_length=150, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.email} {self.name} {self.comment}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
