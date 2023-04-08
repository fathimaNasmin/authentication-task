from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor
from django.forms import RadioSelect

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    profile_picture = forms.ImageField()
    address_line1 = forms.CharField(max_length=255)
    address_city = forms.CharField(max_length=255)
    address_state = forms.CharField(max_length=255)
    address_pincode = forms.CharField(max_length=6)
    role = forms.ChoiceField(label="Sign Up As", widget=forms.RadioSelect, choices=(('patient', 'Patient'), ('doctor', 'Doctor')))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profile_picture',
                  'address_line1', 'address_city', 'address_state', 'address_pincode','role']

    def clean(self):
        cleaned_data = super().clean()
        if 'role' not in cleaned_data:
            raise forms.ValidationError('Please select a role.')
        if cleaned_data['role'] == 'patient':
            cleaned_data['is_patient'] = True
            cleaned_data['is_doctor'] = False
        elif cleaned_data['role'] == 'doctor':
            cleaned_data['is_patient'] = False
            cleaned_data['is_doctor'] = True
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.profile_picture = self.cleaned_data['profile_picture']
        user.address_line1 = self.cleaned_data['address_line1']
        user.address_city = self.cleaned_data['address_city']
        user.address_state = self.cleaned_data['address_state']
        user.address_pincode = self.cleaned_data['address_pincode']
        user.is_patient = self.cleaned_data['is_patient']
        user.is_doctor = self.cleaned_data['is_doctor']
        if commit:
            user.save()
        if user.is_patient:
            patient = Patient(user=user)
            if commit:
                patient.save()
        if user.is_doctor:
            doctor = Doctor(user=user)
            if commit:
                doctor.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )
    ROLE = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    role = forms.ChoiceField(
        label="Login As",
        choices=ROLE,
        widget=forms.RadioSelect,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username doesn't exists")
        return username
