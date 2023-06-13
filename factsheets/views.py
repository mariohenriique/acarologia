from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.db.models import Max,Min
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from folium import Marker,Map
from datetime import date
from PIL import Image
import os

from factsheets.models import Imagens,InformacaoFamilias
from .forms import FactsheetsForm,FactsheetsUpdateForm
from formulario.models import Colecao

# Create your views here.

class FactSheets(TemplateView):
    template_name = 'factsheets.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['family_list'] = Colecao.objects.values('family').distinct().order_by('family').exclude(family='')
        return context

class FactSheetsFamilia(TemplateView):
    template_name = 'factsheets_familia.html'
    # Função que gera o mapa
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Gera somente a div do mapa
        context['map'] = mark_safe(self.fazer_mapa())
        return render(request,self.template_name,context)

    def get_context_data(self, **kwargs):
        family = self.kwargs['family']
        context = super().get_context_data(**kwargs)
        distinct_genera = Colecao.objects.filter(family=family).order_by("genus").exclude(genus='').values('genus').distinct()

        context['genetic_data'] = Colecao.objects.filter(family=family).exclude(genus='').exclude(associatedSequences='').order_by('associatedSequences')
        context['genera'] = Colecao.objects.filter(genus__in=distinct_genera).values('genus').distinct().order_by('genus')
        context['species'] = Colecao.objects.filter(genus__in=context['genera']).values('genus','scientificName').distinct()
        context['family_data'] = InformacaoFamilias.objects.filter(familia=family)
        context['imagens'] = Imagens.objects.filter(familia=family)
        return context

    def fazer_mapa(self):
        family = self.kwargs['family']
        zoom_level = 4
        colecoes = Colecao.objects.filter(family=family)

        # Lista com o maior e menor valor de latitude e longitude
        latitude_values = list(Colecao.objects.filter(family=family).aggregate(Max('decimalLatitude'),Min('decimalLatitude')).values())
        longitude_values = list(Colecao.objects.filter(family=family).aggregate(Max('decimalLongitude'),Min('decimalLongitude')).values())

        if latitude_values == [None,None] and longitude_values == [None,None]:
            latitude_values = [-19.8688655,-19.8688655]
            longitude_values = [-43.9695513,-43.9695513]
            zoom_level = 16

        # média de onde será o meio do mapa
        latitude_media = (sum(latitude_values))/2
        longitude_media = (sum(longitude_values))/2

        mapa_family = Map(location=[latitude_media,longitude_media],zoom_start=zoom_level,tiles='Stamen Terrain')
        for colecao in colecoes:
            if colecao.decimalLatitude and colecao.decimalLongitude:
                latitude = colecao.decimalLatitude
                longitude = colecao.decimalLongitude
                texto_popup = f"UFMG-AC{colecao.catalogNumber}\n{colecao.country} ({colecao.countryCode}), {colecao.stateProvince},{colecao.county},\n {colecao.decimalLatitude};{colecao.decimalLongitude},\n{colecao.eventDate}, Col.: , Cod.: {colecao.associatedSequences}"
                # Escolher o que vai ser colocado no popup
                Marker([latitude, longitude],popup = texto_popup).add_to(mapa_family)
        return mapa_family._repr_html_()

# Adicionar novo factsheets

class FactsheetsCreate(LoginRequiredMixin,CreateView,):
    form_class = FactsheetsForm
    login_url = reverse_lazy('login')
    model = InformacaoFamilias
    template_name = 'add_factsheets.html'
    success_url = reverse_lazy('factsheets')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            factsheet_familia = form.save(commit=False)
            factsheet_familia.dados_geneticos = self.request.POST.getlist('dados_geneticos')
            factsheet_familia = form.save()

            for image_number in range(0, self.request.POST.get('image-count') if type(self.request.POST.get('image-count')) == int else 1):
                image = request.FILES.get(f'imagens-{image_number}-image')
                legend = request.POST.get(f'imagens-{image_number}-legenda')
                if image:
                    path = os.path.join(settings.BASE_DIR,'static','factsheets',request.POST.get('familia'))
                    if not os.path.exists(path):
                        os.makedirs(path)
                    img = Image.open(image)
                    image_name = str(date.today())+'id'+str(image_number)+image.name
                    path_img = os.path.join('factsheets',request.POST.get('familia'),image_name)
                    all_path_img = os.path.join('static',path_img)
                    img.save(all_path_img)
                    new_image = Imagens(post=factsheet_familia, familia=factsheet_familia.familia, imagens=path_img, legenda=legend)
                    new_image.save()
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

# UPDATE factsheets

class FactsheetsUpdate(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'update_factsheets.html'
    form_class = FactsheetsUpdateForm
    model = InformacaoFamilias
    success_url = reverse_lazy('factsheets')

    def form_valid(self, form):
        delete_images = self.request.POST.getlist('delete_image')
        if delete_images:
            for delete_image_id in delete_images:
                try:
                    image = Imagens.objects.get(pk=delete_image_id)
                    path_delete_image = os.path.join(settings.BASE_DIR,'static',str(image.imagens))
                    if os.path.exists(path_delete_image):
                        os.remove(path_delete_image)
                    image.delete()
                except Imagens.DoesNotExist:
                    pass
            messages.success(self.request, 'Images deleted successfully.')
            form = self.get_form()

        if form.is_valid():
            family = form.save(commit=False)
            lista_dados_geneticos=[]
            for i in self.request.POST.getlist('dados_geneticos'):
                lista_dados_geneticos.append(i)
            family.dados_geneticos=lista_dados_geneticos
            family = form.save()
            for image_id in range(0, self.request.POST.get('image-count') if type(self.request.POST.get('image-count')) == int else 1):
                image = self.request.FILES.get(f'imagens-{image_id}-image')
                legend = self.request.POST.get(f'imagens-{image_id}-legenda')
                if image:
                    path = os.path.join(settings.BASE_DIR,'static','factsheets',self.request.POST.get('familia'))
                    if not os.path.exists(path):
                        os.makedirs(path)
                    img = Image.open(image)
                    image_name = str(date.today())+'id'+str(i)+image.name
                    path_img = os.path.join('factsheets',self.request.POST.get('familia'),image_name)
                    all_path_img = os.path.join('static',path_img)
                    img.save(all_path_img)
                    new_image = Imagens(post=family, familia=family.familia, imagens=path_img, legenda=legend)
                    new_image.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        family_id = self.kwargs['pk']
        family_name = InformacaoFamilias.objects.filter(id=family_id).values_list('familia')
        context = super().get_context_data(**kwargs)
        context['images'] = Imagens.objects.filter(familia__in=family_name)
        return context