from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm

@login_required
def profile_view(request):
    # Ensure profile exists (signal should create it, but fallback just in case)
    profile = getattr(request.user, 'profile', None)
    if not profile:
        from .models import Profile
        profile = Profile.objects.create(user=request.user, display_name=request.user.username)
        
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
