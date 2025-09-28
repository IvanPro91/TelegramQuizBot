from django import forms
from django.forms import ModelForm

from users.models import User


class UserProfileForm(ModelForm):
    email = forms.CharField(disabled=True)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["avatar"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = "first_name", "last_name", "email", "avatar"
