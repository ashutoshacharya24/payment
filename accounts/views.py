from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong..')
            return redirect('register')
    form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registration.html', context)

def login_view(request):
    next = None
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                return redirect('home')
            else:
                messages.warning(request, 'Email or password is wrong')
                return redirect('login')
        else:
            messages.error(
                request, 'Something went wrong!! Please try again later')
            return redirect('login')
    form = UserLoginForm()
    if 'next' in request.GET:
        next = request.GET['next']
    context = {
        'form': form,
        'next': next
    }
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')