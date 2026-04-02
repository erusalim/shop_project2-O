from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')

        allowed_domains = ['gmail.com', 'mail.ru']
        if email:
            domain = email.split('@')[-1].lower()
            if domain not in allowed_domains:
                raise forms.ValidationError('Используйте email на gmail.com или mail.ru.')

        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'city', 'address')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите город'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'rows': 3}),
        }
