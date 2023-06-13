from django.urls import path
from .views import *

urlpatterns = [
    #path('endereço/', PacoteView.as_view(),name='nome_da_url'),
    path('',PaginaInicial.as_view(),name='homepage'),
    path('equipe/',Equipe.as_view(),name='equipe'),
]
