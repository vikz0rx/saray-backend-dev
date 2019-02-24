from django.contrib import admin
from mediumeditor.admin import MediumEditorAdmin
from .models import News

@admin.register(News)
class NewsAdmin(MediumEditorAdmin, admin.ModelAdmin):
   list_display = ['title', 'created_at']

   mediumeditor_fields = ('text', )