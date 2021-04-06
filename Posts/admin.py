from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
