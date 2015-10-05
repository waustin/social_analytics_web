from django import forms
import datetime

# Add your forms here

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field


class DataFileUploadForm(forms.Form):
    client = forms.CharField(max_length=75, label="Client's Name")
    data_file = forms.FileField(help_text='An Analytics Data File. Must be in .CSV Format')

    def __init__(self, *args, **kwargs):
        super(DataFileUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('client'),
            Field('data_file'),
            Submit('submit', 'Submit', css_class='button'),
        )


class GraphAPIForm(forms.Form):
    page_url = forms.URLField(help_text='URL for the FB Page.')
    start_date = forms.DateField(initial=datetime.datetime.now,
                                 widget=forms.DateInput(format='%m/%d/%Y'))
    end_date = forms.DateField(initial=datetime.datetime.now,
                               widget=forms.DateInput(format='%m/%d/%Y'))

    def __init__(self, *args, **kwargs):
        super(GraphAPIForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('page_url'),
            Div(Field('start_date'),
                Field('end_date'),
                css_class='date-range'),
            Submit('submit', 'Submit', css_class='button')
        )
