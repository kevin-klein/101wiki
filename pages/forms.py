from django import forms
from .models import Page

class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=100)
    search.widget.attrs.update({'class': 'form-control mr-sm-2'})

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'raw_content']

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['raw_content'].widget.attrs.update({'class' : 'form-control'})
