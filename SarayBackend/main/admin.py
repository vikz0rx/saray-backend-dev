from datetime import datetime, date, time

from django.contrib import admin
from django.utils.html import format_html

from PIL import Image
from mediumeditor.admin import MediumEditorAdmin

from .models import *
from .notifications import *

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
        exclude = ('last_login', 'user_permissions', )

        if request.user.is_staff and request.user == obj:
            exclude += ('is_staff', 'is_superuser', 'groups', 'bonus', 'bonus_amount', 'passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', 'is_active', )

            return exclude

        if obj:
            exclude += ('password', )
            if obj.is_staff:
                exclude += ('bonus', 'bonus_amount', 'passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', )
            else:
                exclude += ('is_staff', 'is_superuser', 'groups', )
        else:
            exclude += ('bonus', 'bonus_amount', 'passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', 'is_active', )
    
        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()

        if request.user.is_staff and request.user == obj:
            return readonly_fields

        if obj:
            readonly_fields += ('username', 'email', 'phone', 'image', 'first_name', 'last_name', 'fathers_name', 'birthdate', )
            if obj.is_staff:
                readonly_fields += ('is_staff', 'is_superuser', 'groups', )

                if not request.user.is_superuser:
                    readonly_fields += ('is_active', )
            else:
                readonly_fields += ('passport_series', 'passport_number', 'insurance', 'sms_notification', 'mail_notification', 'allow_to_use_photos', 'is_active', )

                if not request.user.is_superuser:
                    readonly_fields += ('bonus', 'bonus_amount', )

        return readonly_fields

@admin.register(Locations)
class LocationsAdmin(MediumEditorAdmin, admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))

    image_tag.short_description = ''

    list_display = ('image_tag', 'title', 'cost', )
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

        if obj:
            if obj.approved and not request.user.is_superuser:
                readonly_fields += ('title', 'desc', 'text', 'image', )

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
        for booking in queryset:
            message = u'Reminder sent\r\n\r\Booking {}\r\n\r\ '.format(booking.id)

            send_mail(message, booking.user.email)
            if booking.user.sms_notification:
                send_sms(message, booking.user.phone)

    send_notification.short_description = 'Отправить повторное уведомление'

    list_display = ('date', 'user', 'location', 'time_start', 'time_end', 'payment_notification', 'reminder_notification', 'cost', 'status', )
    inlines = (MultipleRawImageBookingsInline, MultipleProcessedImageBookingsInline, )
    actions = ('send_notification', )

    def get_exclude(self, request, obj=None):
        exclude = ()

        if not obj:
            exclude += ('status', 'payment_notification', 'reminder_notification', 'cost', 'bonus_used', )

        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()

        if obj:
            readonly_fields += ('user', 'status', 'payment_notification', 'reminder_notification', 'cost', 'bonus_used', )

        return readonly_fields

    def save_model(self, request, obj, form, change):
        obj.save()

        booking_total = int((datetime.combine(obj.date, obj.time_end) - datetime.combine(obj.date, obj.time_start)).total_seconds() / 3600)
        booking_cost = 0

        booking_cost += obj.location.cost * booking_total
        booking_cost += obj.types.cost
        booking_cost += obj.photograph.cost * booking_total if obj.photograph else booking_cost
        booking_cost += obj.location.over_week_cost * booking_total if obj.date.weekday() > 5 else booking_cost
        booking_cost += obj.location.over_time_cost * booking_total if obj.time_start > time(22, 00) else booking_cost
        booking_cost -= obj.bonus_used

        for option in obj.options.all():
            booking_cost += option.cost * booking_total

        obj.cost = booking_cost
        obj.save()

        if not change:
            message = '{} - {}'.format(obj.id, obj.user)
            send_mail(message, obj.user.email)
            send_sms(message, obj.user.phone) if obj.user.sms_notification else 0

            obj.user.bonus_amount += int(obj.cost * {SarayUser.BONUS_CLASSIC: .03, SarayUser.BONUS_SILVER: .07, SarayUser.BONUS_GOLD: .15, SarayUser.BONUS_PLATINUM: .20}.get(obj.user.bonus)) - obj.bonus_used

            user_booking_total = 0
            for booking in Bookings.objects.filter(user=obj.user):
                    hours = datetime.combine(booking.date, booking.time_end) - datetime.combine(booking.date, booking.time_start)
                    hours = int(hours.total_seconds() / 3600)
                    user_booking_total += hours
            
            if user_booking_total >= 150:
                obj.user.bonus = SarayUser.BONUS_PLATINUM
            elif user_booking_total >= 70:
                obj.user.bonus = SarayUser.BONUS_GOLD
            elif user_booking_total >= 20:
                obj.user.bonus = SarayUser.BONUS_SILVER
            else:
                obj.user.bonus = SarayUser.BONUS_CLASSIC

            obj.user.save()