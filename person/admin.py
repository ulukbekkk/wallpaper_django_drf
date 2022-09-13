from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_image')
    readonly_fields = ("get_image",)

    # Выводит фото в админ понели
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    # Дает название к таблицам изображений
    get_image.short_description = 'Изображение'

admin.site.register(User, UserAdmin)
