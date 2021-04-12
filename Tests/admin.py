from django.contrib import admin
from django.utils.html import format_html

from .models import *

class TestModelAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']

    class Meta:
        model = Test
    

class TestTaskModelAdmin(admin.ModelAdmin):
    list_display = ['test_id', 'title', 'type', 'points']
    list_display_links = ['title']
    list_filter = ['title', 'points']
    search_fields = ['title']

    class Meta:
        model = TestTask


class UserTestModelAdmin(admin.ModelAdmin):
    list_display = ['test_id', 'result_points', 'check_status']
    list_display_links = ['test_id']
    list_filter = ['result_points']

    class Meta:
        model = UserTest


class UserTestTaskModelAdmin(admin.ModelAdmin):
    list_display = ['user_test_id', 'title', 'type', 'points', 'user_points', 'check_status']
    list_display_links = ['title']
    list_filter = ['title', 'points', 'user_points']
    search_fields = ['title']

    class Meta:
        model = UserTestTask


class CreateTestModelAdmin(admin.ModelAdmin):
    list_display = ['show_url']

    def show_url(self):
        return format_html("<a href='{url}'>Создать тест</a>", url='/create_test/')

    show_url.short_description = 'Создать тест'

admin.site.register(Test, TestModelAdmin)
admin.site.register(TestTask, TestTaskModelAdmin)
admin.site.register(UserTest, UserTestModelAdmin)
admin.site.register(UserTestTask, UserTestTaskModelAdmin)
admin.site.register()
