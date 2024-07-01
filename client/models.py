from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Ф.И.О',
        **NULLABLE
    )
    comment = models.CharField(
        max_length=150,
        verbose_name='комментарий',
        **NULLABLE
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='cоздатель',
        **NULLABLE,
    )

    def __str__(self):
        return f'{self.email} {self.name} {self.comment}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
