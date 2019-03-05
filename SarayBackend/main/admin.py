from django.contrib import admin
from django.utils.html import format_html

from mediumeditor.admin import MediumEditorAdmin

from .models import *

class MultipleImagePhotographsInline(admin.TabularInline):
    model = MultipleImagePhotographs
    extra = 5

class MultipleImageLocationsInline(admin.TabularInline):
    model = MultipleImageLocations
    extra = 5

class MultipleRawImageBookingsInline(admin.TabularInline):
    model = MultipleRawImageBookings
    extra = 10

class MultipleProcessedImageBookingsInline(admin.TabularInline):
    model = MultipleProcessedImageBookings
    extra = 10

@admin.register(SarayUser)
class SarayUserAdmin(admin.ModelAdmin):
    def phone_refactored(self, obj):
        if obj.phone:
            return '+' + obj.phone[0] + '(' + obj.phone[1:4] + ')' + obj.phone[4:7] + '-' + obj.phone[7:]
        return '-'

    def name_refactored(self, obj):
        if obj.first_name and obj.last_name and obj.fathers_name:
            return obj.last_name + ' ' + obj.first_name + ' ' + obj.fathers_name
        elif obj.first_name and obj.last_name:
            return obj.first_name + ' ' + obj.last_name
        else:
            return obj.username

    phone_refactored.short_description = 'Номер телефона'
    name_refactored.short_description = 'Ф.И.О.'

    list_display = ('name_refactored', 'phone_refactored', 'email', 'birthdate', )
    search_fields = ('last_name', )

    def get_exclude(self, request, obj=None):
        exclude = ('password', 'last_login', 'user_permissions', 'is_superuser', 'groups')
        if not request.user.is_superuser:
            exclude += ('is_staff', )

        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('bonus_amount', 'username', 'email', 'phone', 'image', 'first_name', 'last_name', 'fathers_name', 'birthdate', 'passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', )
        if request.user.is_superuser:
            readonly_fields += ('is_staff', )
        else:
            readonly_fields += ('is_active', 'bonus', )

        return readonly_fields

@admin.register(Locations)
class LocationsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))

    image_tag.short_description = ''

    list_display = ('title', 'cost', 'image_tag', )
    inlines = (MultipleImageLocationsInline, )
    mediumeditor_fields = ('text', )

@admin.register(Photographs)
class PhotographsAdmin(admin.ModelAdmin):
    list_display = ('link', 'first_name', 'last_name', )
    inlines = (MultipleImagePhotographsInline, )

@admin.register(News)
class NewsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))
    
    image_tag.short_description = 'Обложка'

    list_display = ('image_tag', 'author', 'title', 'created_at', 'approved', )
    search_fields = ('title', )
    mediumeditor_fields = ('text', )

    def get_exclude(self, request, obj=None):
        exclude = ()
        if not request.user.is_superuser:
            exclude += ('author', )
        
        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        if not request.user.is_superuser:
            readonly_fields += ('approved', )
        else:
            readonly_fields += ('author', )

        return readonly_fields

    def get_queryset(self, request):
        if request.user.is_superuser:
            return News.objects.all()
        return News.objects.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

@admin.register(BookingTypes)
class BookingTypesAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'cost', )

@admin.register(BookingOptions)
class BookingOptionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'cost', )


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    def send_notification(self, request, queryset):
        SMS_API = '8BF374E2-915E-C59E-28D3-DA429B13E441'

        for booking in queryset:
            # Send EMail

            if booking.user.sms_notification:
                phone = booking.user.phone
                message = u'Бронирование №{}, Пользователь - {}'.format(booking.id, booking.user)
                req = 'https://sms.ru/sms/send?api_id={}&to={}&msg={}'.format(SMS_API, phone, message)

    send_notification.short_description = 'Отправить повторное уведомление'

    list_display = ('id', 'date', 'user', 'location', 'time_start', 'time_end', 'payment_notification', 'reminder_notification', 'cost', 'status', )
    inlines = (MultipleRawImageBookingsInline, MultipleProcessedImageBookingsInline, )
    actions = ('send_notification', )

    def get_exclude(self, request, obj=None):
        exclude = ()
        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('user', 'status', 'payment_notification', 'reminder_notification', 'cost', 'bonus_used', )
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()

            obj.payment_notification = True
            obj.user.bonus_amount += int(obj.cost * {SarayUser.BONUS_CLASSIC: .03, SarayUser.BONUS_SILVER: .07, SarayUser.BONUS_GOLD: .15, SarayUser.BONUS_PLATINUM: .20}.get(obj.user.bonus)) - obj.bonus_used

            # Bonus card
            if True:
                obj.user.bonus = SarayUser.BONUS_PLATINUM
            elif True:
                obj.user.bonus = SarayUser.BONUS_GOLD
            elif True:
                obj.user.bonus = SarayUser.BONUS_SILVER
            else:
                obj.user.bonus = SarayUser.BONUS_CLASSIC

            obj.user.save()

        cost = 0
        cost += obj.location.cost

        if obj.date.weekday() > 5:
            cost += obj.location.over_week_cost

        # if obj.time_start:
        #     cost += obj.location.over_time_cost

        cost += obj.types.cost
        cost -= obj.bonus_used

        for item in obj.options.all():
            cost += item.cost

        if obj.photograph:
            cost += obj.photograph.cost

        obj.cost = cost

        obj.save()