from django.contrib import admin
from mediumeditor.admin import MediumEditorAdmin
from .models import SarayUser ,News

@admin.register(SarayUser)
class SarayUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']

    mediumeditor_fields = ('text', )

@admin.register(News)
class NewsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    list_display = ['title', 'created_at']

    mediumeditor_fields = ('text', )