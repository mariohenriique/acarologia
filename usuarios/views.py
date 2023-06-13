from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.

class Login(TemplateView):
    template_name = 'login.html'

class PaginaUsuario(TemplateView):
    template_name = 'usuario.html'

class AlteracaoSenha(TemplateView):
    template_name = 'alterar_senha.html'