from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    plan = request.GET.get('plan')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly specify the backend to avoid multiple backend error
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registration successful! Welcome to Finance Tracker.')
            
            # Check if user selected premium plan
            if plan == 'premium':
                return redirect('payments:upgrade')
                
            return redirect('dashboard:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    """Display user profile."""
    return render(request, 'accounts/profile.html')
