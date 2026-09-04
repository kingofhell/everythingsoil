from django.shortcuts import render, get_object_or_404
from .models import Element, Article

def home(request):
    elements = Element.objects.filter(is_active=True)[:5]
    latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
    return render(request, 'soil/home.html', {
        'elements': elements,
        'latest_articles': latest_articles
    })

def soil_detail(request):
    return render(request, 'soil/soil_detail.html')

def panja_bootham(request):
    elements = Element.objects.filter(is_active=True)
    return render(request, 'soil/panja_bootham.html', {'elements': elements})

def element_detail(request, slug):
    element = get_object_or_404(Element, slug=slug, is_active=True)
    # Get current user preferred language if logged in, default to English
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.profile.preferred_language
    
    translation = element.translations.filter(language=lang).first()
    # Fallback to English translation if language translation is missing
    if not translation and lang != 'en':
        translation = element.translations.filter(language='en').first()
        
    return render(request, 'soil/element_detail.html', {
        'element': element,
        'translation': translation
    })

def lingeswarar(request):
    return render(request, 'soil/lingeswarar.html')

def about(request):
    return render(request, 'soil/about.html')
