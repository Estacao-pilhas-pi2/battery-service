from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    dataNascimento = models.DateField(null=True)
    telefone = PhoneNumberField(null=True)
    nome = models.CharField(max_length=80)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
