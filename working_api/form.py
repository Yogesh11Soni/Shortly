from django import forms
from working_api.models import URL, URLWithCredentials


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        exclude = ['t_id', 'full_url', 'url_hash', 'created_at']



class URLCredentialsLForm(forms.ModelForm):
    class Meta:
        model = URLWithCredentials
        exclude = ['t_id', 'full_url', 'url_hash', 'created_at', 'u_id']
