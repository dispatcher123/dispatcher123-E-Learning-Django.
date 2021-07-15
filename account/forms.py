from django import forms
from django.forms import fields
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        'class' : 'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password',
    }))

    class Meta:
        model=CustomUser
        fields=('email','first_name','last_name')

    
    def clean(self):
        cleaned_data=super(RegistrationForm, self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password !=confirm_password:
            raise forms.ValidationError('Password Does Not Match!')

    
    def __init__(self,*args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['first_name'].widget.attrs['placeholder']='Enter Email'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
