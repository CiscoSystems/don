from django import forms

class PingForm(forms.Form):
    src_ip = forms.CharField(label='Source IP', max_length=30,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    dst_ip = forms.CharField(label='Destination IP', max_length=30,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    router = forms.CharField(label='Router', max_length=30,widget=forms.TextInput(attrs={'class' : 'form-control'}))
