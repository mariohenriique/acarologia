from django.utils import timezone
from django import forms

from factsheets.models import InformacaoFamilias
from formulario.models import Colecao

def get_choice_familia():
    # Excluir da lista de choices se existir registro para a família
    exclude = ['']
    families_with_records = list(InformacaoFamilias.objects.values_list('familia',flat=True))
    exclude += families_with_records

    available_families = Colecao.objects.order_by('family').values_list('family',flat=True).distinct().exclude(family__in=exclude)
    choices = [(family,family) for family in available_families]
    return choices

def get_ano_choice():
    choices = [(year,year) for year in range(timezone.now().year,1850,-1)]
    return choices

# Verificar o que vai ser excluido e o que vai ser mostrado
def get_dado_geneticos():
    excluir=['']
    genetic = Colecao.objects.exclude(family__in=excluir).order_by('catalogNumber')
    choice = [(r,r) for r in genetic]
    return choice

class FactsheetsForm(forms.ModelForm):
    ano = forms.ChoiceField(choices=get_ano_choice)
    autor = forms.CharField(max_length=50)
    caracteristicas_gerais = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    dados_geneticos = forms.MultipleChoiceField(choices=get_dado_geneticos,widget=forms.SelectMultiple)
    diagnoses = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    familia = forms.ChoiceField(label='Família',choices=get_choice_familia)
    referencias = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = InformacaoFamilias
        fields = ['familia','autor','ano','dados_geneticos','diagnoses','caracteristicas_gerais','referencias']
    # Conferir esta parte
    def save(self, commit=True):
        familia = super().save(commit=False)
        if commit:
            familia.save()

        imagens = self.cleaned_data.get('imagens')
        legendas = self.cleaned_data.get('legendas').splitlines() if self.cleaned_data.get('legendas') else []
        if imagens:
            for i, imagem in enumerate(imagens):
                legenda = legendas[i] if i < len(legendas) else ''
                familia.imagens.create(image=imagem, legenda=legenda)
        return familia

class FactsheetsUpdateForm(forms.ModelForm):
    dados_geneticos = forms.MultipleChoiceField(choices=get_dado_geneticos,widget=forms.SelectMultiple)
    class Meta:
        model = InformacaoFamilias
        fields = ['familia','autor','ano','dados_geneticos','diagnoses','caracteristicas_gerais','referencias']
        # widget={
        #     'ano':'',
        #     'autor':'',
        #     'caracteristicas_gerais':'',
        #     'dados_geneticos':'',
        #     'diagnoses':'',
        #     'familia':'',
        #     'imagens':'',
        #     'legenda':'',
        #     'referencias':'',
        # }