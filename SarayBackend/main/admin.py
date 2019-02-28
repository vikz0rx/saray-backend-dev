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
    exclude = ('last_login', )

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.exclude += ('last_login', )

            if obj.is_staff:
                self.exclude += ('bonus', 'birthdate', 'passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', )

        return super(SarayUserAdmin, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('last_login', 'is_superuser', 'is_staff', 'groups', )
        not_user_fields = ('username', 'email', 'phone', 'image', 'firstname', 'lastname', 'fathersname', 'birthdate', 'passport_series', 'passport_number', 'insurance', )
        notification_fields = ('sms_notification', 'mail_notification', 'allow_to_use_photos', )

        if obj:
            if request.user != obj:
                if request.user.is_superuser:
                    return not_user_fields + notification_fields + readonly_fields
                elif request.user.is_staff:
                    return not_user_fields + ('bonus', ) + notification_fields + readonly_fields + ('is_active', )
                else:
                    return not_user_fields + ('bonus', ) + notification_fields + readonly_fields + ('is_active', )
            else:
                if request.user.is_superuser:
                    return readonly_fields
                elif request.user.is_staff:
                    return readonly_fields
                else:
                    return readonly_fields
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


        # BONUS CARD SELECTION

        overall_sum = 0

        for item in Bookings.objects.filter(user=obj.user):
            overall_sum += item.cost

        if overall_sum >= 70000:
            obj.user.bonus = SarayUser.BONUS_PLATINUM
            obj.user.save()
        elif overall_sum >= 50000:
            obj.user.bonus = SarayUser.BONUS_GOLD
            obj.user.save()
        elif overall_sum >= 30000:
            obj.user.bonus = SarayUser.BONUS_SILVER
            obj.user.save()
        else:
            obj.user.bonus = SarayUser.BONUS_CLASSIC
            obj.user.save()

    actions = ['send_notification']
    list_display = ['user', 'date', 'location', 'image_tag', 'time_start', 'time_end', 'payment_notification', 'reminder_notification', 'cost', 'status']
    readonly_fields = ('payment_notification', 'reminder_notification', 'cost', ) # 'user'