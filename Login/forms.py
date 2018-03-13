from django.contrib.auth.models import User
from django import forms
from .models import song_album,song

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']

class AlbumForm(forms.ModelForm):

    class Meta:
        model = song_album
        fields = ['artist','albub_title','genre','album_logo']


class SongForm(forms.ModelForm):
    class Meta:
        model = song
        fields = ['song_title', 'audio_file']