from django import forms


class UploadImgForm(forms.Form):
    img = forms.ImageField()

    def __str__(self):
        return self.img
#
