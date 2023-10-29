from django import forms
from projects.models import Categories, Projects

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'details', 'category', 'total_target', 'start_campaign', 'end_campaign']
