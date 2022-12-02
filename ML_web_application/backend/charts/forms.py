from django import forms
from .models import upload_model
#DataFlair #File_Upload
class Upload_Form(forms.ModelForm):
    class Meta:
        model = upload_model
        fields = [
        'data_file'
        ]