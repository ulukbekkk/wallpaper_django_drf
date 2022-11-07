from django.contrib import admin
from .models import MyRoom

from django.utils.safestring import mark_safe


class MyRoomAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'get_image')
    readonly_fields = ("get_image",)

    # Выводит фото в админ понели
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    # Дает название к таблицам изображений
    get_image.short_description = 'Изображение'


admin.site.register(MyRoom, MyRoomAdmin)

