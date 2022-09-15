from django.contrib import admin
from .models import Category, Wallpaper, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title', )
    search_fields = ('title', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Wallpaper)
admin.site.register(Comment)
# Register your models here.
