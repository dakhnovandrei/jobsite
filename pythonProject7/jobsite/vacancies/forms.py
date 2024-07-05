from django import forms

class VacancySearchForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название вакансии', required=False)