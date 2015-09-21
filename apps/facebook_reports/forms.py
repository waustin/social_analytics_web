from django import forms
# Add your forms here

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field


class DataFileUploadForm(forms.Form):
    client = forms.CharField(max_length=75)
    data_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(DataFileUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('client'),
            Field('data_file'),
             Submit('submit', 'Submit', css_class='button'),
        )
