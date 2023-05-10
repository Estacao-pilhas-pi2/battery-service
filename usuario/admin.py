from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from usuario.models import Usuario


class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'cpf', 'nome', 'telefone')
    ordering = ('email',)


admin.site.register(Usuario, UsuarioAdmin)
