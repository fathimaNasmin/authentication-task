from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, LoginForm
from .models import User,Patient,Doctor



def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data['role'])
            print('success')
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('signup')
            # login(request, user)
            # if user.is_patient:
            #     return redirect('patient_dashboard')
            # if user.is_doctor:
            #     return redirect('doctor_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})



def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = authenticate(request, username=username, password=password)
            print(username, role)
            if user is not None:
                if role == 'patient' and user.is_patient:
                    login(request, user)
                    return redirect('patient_dashboard')
                elif role == 'doctor' and user.is_doctor:
                    login(request, user)
                    return redirect('doctor_dashboard')

            print('Invalid username or password')
            messages.error(request, "User doesn't exists")
            return redirect('login')
    return render(request, 'login.html', {'form':form})


@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')


@login_required
def patient_dashboard(request):
    current_user = request.user
    print(current_user)
    return render(request, 'patient_dashboard.html')


def logout_user(request):
    logout(request)
    return redirect('home')