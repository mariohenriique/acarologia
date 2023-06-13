from django.urls import path

# importar as classes no pacote views
from .views import *

urlpatterns = [
    #path('endereço/', PacoteView.as_view(),name='nome_da_url'),
    path('cadastrar/avancado/colecao/',ColecaoAvancadoCreate.as_view(),name='cadastrar_avancado_colecao'),
    path('cadastrar/csv/colecao/',ColecaoCSVCreate.as_view(),name='cadastrar_csv_colecao'),
    path('editar/colecao/<int:pk>/',ColecaoUpdate.as_view(),name='editar_colecao'),
    path('cadastrar/colecao/',ColecaoCreate.as_view(),name='cadastrar_colecao'),
    path('listar/colecao/',ColecaoList.as_view(),name='listar_colecao'),
    path('confirma/tombo/',TomboList.as_view(),name='confirma_tombo'),
    path('modelo/',Download_Modelo.colecao_csv,name='baixa_modelo'),
    path('download/',Download.colecao_csv,name='baixa'),
]