from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ClearableFileInput, FileInput, ModelForm, TextInput
from .models import Profile


class ProfileCreateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': FileInput(attrs={
                'class': 'pt_btn1',
            }),
        }


class AccountUpdateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['nickname'].disabled = True
