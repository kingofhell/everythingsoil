from django import forms
from .models import Profile, Interest

class ProfileForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'profile_image', 'preferred_language', 'interests']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'preferred_language': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['interests'].initial = self.instance.interests.all()

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            self.save_m2m()  # Saves many-to-many relationships (interests)
        return profile
