from django.contrib import admin
from .models import *


@admin.register(Brokers)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'mail', 'iscompany')
    search_fields = ('fullname',)
    list_editable = ('iscompany',)
    list_per_page = 25


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'chat_id', 'status')
    list_editable = ('status',)
    search_fields = ('first_name', 'last_name')
    list_filter = ('status',)
    list_per_page = 50


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'current_location', 'destination', 'planned_time', 'eta', 'eta_status', 'status', 'link', 'live_share',
        'updated_at', 'broker')
    list_filter = ('eta_status', 'eta', 'broker', 'updated_at', 'status')
    search_fields = ('name',)
    # exclude = ('vehicle_id',)
    readonly_fields = ('eta', 'eta_status', 'updated_at', 'link', 'live_share', 'current_location', 'status')
    list_editable = ('destination', 'planned_time', 'broker')
    list_per_page = 50


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    search_fields = ('title',)
    list_filter = ('title', )
    list_per_page = 50

