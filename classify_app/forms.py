from django import forms


class UploadImgForm(forms.Form):
    img = forms.ImageField()
#
