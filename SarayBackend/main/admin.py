from django.contrib import admin
from django.utils.html import format_html
from mediumeditor.admin import MediumEditorAdmin
from .models import *

@admin.register(SarayUser)
class SarayUserAdmin(admin.ModelAdmin):
    def phone_refactored(self, obj):
        if obj.phone:
            return '+' + obj.phone[0] + '(' + obj.phone[1:4] + ')' + obj.phone[4:7] + '-' + obj.phone[7:]
        return '-'

    phone_refactored.short_description = 'Номер телефона'

    def name_refactored(self, obj):
        if obj.firstname and obj.lastname and obj.fathersname:
            return obj.lastname + ' ' + obj.firstname + ' ' + obj.fathersname
        elif obj.firstname and obj.lastname:
            return obj.firstname + ' ' + obj.lastname
        else:
            return obj.username

    name_refactored.short_description = 'ФИО'

    list_display = ['name_refactored', 'phone_refactored', 'email', 'birthdate']
    search_fields = ('lastname', )

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('username', 'is_superuser', 'user_permissions', 'groups', 'password', 'is_active', 'is_staff', 'last_login')
        else:
            self.exclude = ('password', 'user_permissions', 'last_login')

        if obj.is_staff:
            self.exclude += ('sms_notification', 'mail_notification', 'allow_to_use_photos')

        return super(SarayUserAdmin, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user != obj:
                if obj.is_staff:
                    return ('last_login', 'username', 'email', 'phone', 'image', 'firstname', 'lastname', 'fathersname', 'birthdate', 'passport_series', 'passport_number', 'insurance', 'is_superuser', 'is_staff', 'groups', )
                else:
                    return ('last_login', 'username', 'email', 'phone', 'image', 'firstname', 'lastname', 'fathersname', 'birthdate', 'passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', 'is_superuser', 'is_staff', 'groups', )
            else:
                return ('last_login', 'is_superuser', 'is_staff', 'groups', )
        else:
            return []

@admin.register(Locations)
class LocationsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))

    image_tag.short_description = ''

    list_display = ['title', 'image_tag']

    mediumeditor_fields = ('text', )

@admin.register(Photographs)
class PhotographsAdmin(admin.ModelAdmin):
    list_display = ['link', 'first_name', 'last_name', 'desc']

@admin.register(News)
class NewsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))
    
    image_tag.short_description = 'Обложка'

    list_display = ['author', 'title', 'created_at', 'image_tag', 'approved']
    readonly_fields = ('author', )
    search_fields = ('title', )

    mediumeditor_fields = ('text', )

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('approved', )
        return super(NewsAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return News.objects.all()
        return News.objects.filter(author=request.user)

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

@admin.register(BookingTypes)
class BookingTypesAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'cost']

@admin.register(BookingOptions)
class BookingOptionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'cost']

@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    def send_notification(self, request, queryset):
        print(request)
        print(queryset)
    
    send_notification.short_description = "Отправить дополнительное уведомление"

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.location.image.url))

    image_tag.short_description = ''

    def save_model(self, request, obj, form, change):
        if not change:
            # SEND SMS / MAIL NOTIFICATION FUNCTION
            obj.payment_notification = True

            # CALCULATE SUM FUNCTION
            sum = 0
            sum += obj.location.cost 
            sum += obj.types.cost 
            # SUM SELECTED OPTIONS
            # print(obj.options.all())
            obj.cost = sum

        obj.save()

    actions = ['send_notification']
    list_display = ['date', 'location', 'image_tag', 'time_start', 'time_end', 'payment_notification', 'reminder_notification', 'cost', 'status']
    readonly_fields = ('payment_notification', 'reminder_notification', 'cost', )