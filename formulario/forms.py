from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Colecao

class ColecaoForm(forms.ModelForm):
    eventDateEnd = forms.DateField(required=False,label='Data do evento final',widget=forms.DateInput(attrs={'type': 'date'}))
    georeferenceDateEnd = forms.DateField(required=False,label='Data georeferenciamento final',widget=forms.DateInput(attrs={'type': 'date'}))
    dateIdentifiedEnd = forms.DateField(required=False,label='Data de identificação final',widget=forms.DateInput(attrs={'type': 'date','min':'{{ today }}'}))
    class Meta:
        model = Colecao
        fields = ['catalogNumber','otherCatalogNumbers','recordedBy','recordNumber','individualCount','sex','lifeStage',
            'reproductiveCondition','preparations','associatedTaxa','associatedReferences','associatedMedia','associatedSequences',
            'occurrenceRemarks','eventDate','eventDateEnd','eventTime','habitat','samplingProtocol','samplingEffort','eventRemarks',
            'continent','country','countryCode','stateProvince','county','municipality','island','islandGroup','waterBody','locality',
            'locationRemarks','minimumElevationInMeters','maximumElevationInMeters','minimumDepthInMeters','maximumDepthInMeters',
            'verbatimLatitude','verbatimLongitude','verbatimCoordinates','decimalLatitude','decimalLongitude',
            'coordinateUncertaintyInMeters','geodeticDatum','georeferenceProtocol','georeferenceBy','georeferenceDate',
            'georeferenceDateEnd','georeferenceRemarks','kingdom','phylum','classe','order','family','subfamily','genus','subgenus',
            'specificEpithet','infraspecificEpithet','scientificName','scientificNameAuthorShip','taxonRank','vernacularName',
            'taxonRemarks','identificationQualifier','typeStatus','identifiedBy','dateIdentified','dateIdentifiedEnd',
            'identificationRemarks']
        if Colecao.objects.last():
            widgets = {
            'eventDate': forms.DateInput(attrs={'type': 'date'}),
            'georeferenceDate': forms.DateInput(attrs={'type': 'date'}),
            'dateIdentified': forms.DateInput(attrs={'type': 'date','id':'dateIdentified'}),
            'eventTime': forms.TimeInput(attrs={'type': 'time'}),
            'catalogNumber': forms.TextInput(attrs={'placeholder': int(str(Colecao.objects.last()))+1}),
        }

class ColecaoEditaForm(forms.ModelForm):
    eventDateEnd = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    georeferenceDateEnd = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    dateIdentifiedEnd = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model=Colecao
        fields = ['basisOfRecord','datasetName','type','language','institutionID','institutionCode','collectionCode',
            'license','rightsHolder','dynamicProperties','occurrenceID','catalogNumber','otherCatalogNumbers','recordedBy',
            'recordNumber','individualCount','sex','lifeStage','reproductiveCondition','preparations','disposition','associatedTaxa',
            'associatedReferences','associatedMedia','associatedSequences','occurrenceRemarks','eventDate','eventTime','habitat',
            'samplingProtocol','samplingEffort','eventRemarks','continent','country','countryCode','stateProvince','county',
            'municipality','island','islandGroup','waterBody','locality','locationRemarks','minimumElevationInMeters',
            'maximumElevationInMeters','minimumDepthInMeters','maximumDepthInMeters','verbatimLatitude','verbatimLongitude',
            'graus','minutos','segundos','Sul_Norte','graus_1','minutos_1','segundos_1','w_O','verbatimCoordinates',
            'decimalLatitude','decimalLongitude','coordinateUncertaintyInMeters','geodeticDatum','georeferenceProtocol',
            'georeferenceBy','georeferenceDate','georeferenceRemarks','kingdom','phylum','classe','order','family','subfamily',
            'genus','subgenus','specificEpithet','infraspecificEpithet','scientificName','scientificNameAuthorShip','taxonRank',
            'vernacularName','taxonRemarks','identificationQualifier','typeStatus','identifiedBy','dateIdentified',
            'dateIdentifiedEnd','identificationRemarks']
        if Colecao.objects.last():
            widgets = {
            'eventDate': forms.DateInput(attrs={'type': 'date'}),
            'georeferenceDate': forms.DateInput(attrs={'type': 'date'}),
            'dateIdentified': forms.DateInput(attrs={'type': 'date'}),
            'eventTime': forms.TimeInput(attrs={'type': 'time'}),
            'catalogNumber': forms.TextInput(attrs={
                'placeholder': int(str(Colecao.objects.last()))+1}),
        }

class CsvForm(forms.ModelForm):
    file = forms.FileField(label='arquivo')
    class Meta:
        model = Colecao
        fields = ['file']