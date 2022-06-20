from django.db import models
from django.contrib import admin
from django.forms.widgets import Textarea

from mptt.admin import DraggableMPTTAdmin

from .models import Tweet

class TweetAdmin(DraggableMPTTAdmin):
    '''
    Класс, представляющий админ-панель для модели твитов.
    '''

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 10, 'cols': 60})},
    }

    list_display = ('tree_actions', 'indented_title', 'user', 'pub_date', 'parent')
    list_filter = ('pub_date',)
    list_select_related = ('user', 'parent')
    search_fields = ('text', 'user__username')
    search_help_text = 'Поиск по тексту твита или имени пользователя'
    show_full_result_count = False
    fieldsets = (
        (None, {
            'fields': ('text', 'user', 'parent'),
            }
        ),
    )

admin.site.register(Tweet, TweetAdmin)


