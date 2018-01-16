from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django import forms

from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from apiclient import discovery
import httplib2
from oauth2client import client

from memryHub import settings

# Create your views here.
def signup(request):
    #validate the form
    form = SignupForm();
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = User()
            u.username = form.cleaned_data.get('username')
            u.email = form.cleaned_data.get('email')
            u.first_name = form.cleaned_data.get('first_name')
            u.last_name = form.cleaned_data.get('last_name')
            u.set_password(form.cleaned_data.get('password'))
            u.save()

            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

            login(request, user)
            return HttpResponseRedirect('/')

    template_vars = {
        'form': form,
    }

    return render(request, 'account/signup.html', template_vars)

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.CharField(label='Email', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    first_name = forms.CharField(label='First Name:', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name:', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    password = forms.CharField(label='Password:', required=True, max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password:', required=True, max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Your passwords do not match')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # check uniqueness of the username
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('This username is already taken. Please try another.')
        return username

def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            # url = request.urlparams[0]
            return HttpResponse('''
                <script>
                    window.location.href = '/'
                </script>
            ''')

    template_vars = {
        'form': form,
    }

    return render(request, 'account/login.html', template_vars)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user == None:
            raise forms.ValidationError('Your username or password is incorrect')
        self.user = user
        return self.cleaned_data

def logout_user(request):
    logout(request)

    return HttpResponseRedirect('/')

def google_login(request):
    if request.method == 'POST':

        auth_code = request.POST['authcode']
        # Set path to the Web application client_secret_*.json file you downloaded from the
        # Google API Console: https://console.developers.google.com/apis/credentials
        CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
            auth_code)

        # # Call Google API
        # http_auth = credentials.authorize(httplib2.Http())
        # drive_service = discovery.build('drive', 'v3', http=http_auth)
        # appfolder = drive_service.files().get(fileId='appfolder').execute()

        print(credentials)
        # Get profile info from ID token
        userid = credentials.id_token['sub']
        email = credentials.id_token['email']

        print(userid, email)
        return HttpResponse('Success')
    return render(request, 'account/google_login.html')
