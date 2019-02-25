from django.contrib import admin
from mediumeditor.admin import MediumEditorAdmin
from .models import SarayUser, Locations, Photographs, News

@admin.register(SarayUser)
class SarayUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']

@admin.register(Locations)
class LocationsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    list_display = ['title']

    mediumeditor_fields = ('text', )

@admin.register(Photographs)
class PhotographsAdmin(admin.ModelAdmin):
    list_display = ['link' ,'first_name', 'last_name', 'desc']

@admin.register(News)
class NewsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    exclude = ('author',)
    list_display = ['author', 'title', 'created_at', 'approved']

    mediumeditor_fields = ('text', )

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('author', 'approved')
        return super(NewsAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return Entry.objects.all()
        return Entry.objects.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(NewsAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(NewsAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True