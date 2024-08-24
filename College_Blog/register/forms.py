# from django import forms
# from . models import Profile
# from django.contrib.auth import get_user_model
# # from django.contrib.auth.models import User
# from django.contrib.auth.hashers import check_password


# class UserRegistrationForm(forms.ModelForm):
   
#     class Meta:
#         model = Profile
#         fields = ['username', 'email', 'password', 'department']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if Profile.objects.filter(username=username).exists():
#             raise forms.ValidationError("This username is already taken.")
#         return username

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if Profile.objects.filter(email=email).exists():
#             raise forms.ValidationError("This email is already registered.")
#         return email

#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         if len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")
#         return password
# class LoginForm(forms.Form):
#     email = forms.EmailField(label='Email Address')
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')

#     # def clean(self):
#     #     cleaned_data = super().clean()
#     #     email = cleaned_data.get('username')
#     #     password = cleaned_data.get('password')

#     #     # Check if the user exists
#     #     try:
#     #         user = User.objects.get(email=email)
#     #     except User.DoesNotExist:
#     #         raise forms.ValidationError('Invalid email or password.')

#     #     # Verify the password
#     #     if not check_password(password, user.password):
#     #         raise forms.ValidationError('Invalid email or password.')
        
#     #     return cleaned_data 
