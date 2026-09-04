from django.contrib import admin
from .models import Element, ElementTranslation, Category, Tag, Article

class ElementTranslationInline(admin.StackedInline):
    model = ElementTranslation
    extra = 2

class ElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'order', 'is_active')
    search_fields = ('name', 'key')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ElementTranslationInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'published_at', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    list_filter = ('status', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'elements')

admin.site.register(Element, ElementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
