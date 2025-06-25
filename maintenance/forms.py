from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Upload CSV')

class AIQueryForm(forms.Form):
    question = forms.CharField(label='Ask the AI Assistant', max_length=300)
