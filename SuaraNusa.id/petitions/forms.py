from django import forms
from django.contrib.auth.models import User
from .models import Petition, City, Province

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password tidak cocok.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class PetitionForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), label="Provinsi", required=True)
    
    class Meta:
        model = Petition
        fields = ['title', 'image', 'description', 'category', 'province', 'city', 'target_support']
        labels = {
            'title': 'Judul Petisi',
            'image': 'Foto Petisi',
            'description': 'Deskripsi/Gagasan',
            'category': 'Kategori',
            'city': 'Kota/Kabupaten',
            'target_support': 'Target Dukungan',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.city.province.cities.order_by('name')
            self.fields['province'].initial = self.instance.city.province
