from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Админка блога"""

    list_display = ('title', 'text', 'image', 'published')
    list_filter = ('title',)
    search_fields = ('title', 'text',)
