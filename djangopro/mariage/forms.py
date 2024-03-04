from django import forms

class FindcustomlistmarForm(forms.Form):
    datemarfrom = forms.CharField(label="تاريخ الزواج من",widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}),)
    datemarto = forms.CharField(label="تاريخ الزواج إلى",widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}),)
