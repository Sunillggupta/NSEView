"""
Django admin configuration for NSE data models.
"""
from django.contrib import admin

from .models import Index, IndexHistory, APIStatus


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'symbol', 'key', 'last_price',
        'change', 'percent_change', 'last_updated',
    )
    list_filter = ('key',)
    search_fields = ('name', 'symbol', 'key')
    ordering = ('name',)
    readonly_fields = ('last_updated', 'created_at')


@admin.register(IndexHistory)
class IndexHistoryAdmin(admin.ModelAdmin):
    list_display = ('index', 'timestamp', 'price', 'change', 'percent_change')
    list_filter = ('index',)
    search_fields = ('index__name', 'index__symbol')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    autocomplete_fields = ('index',)


@admin.register(APIStatus)
class APIStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint', 'status', 'last_checked')
    list_filter = ('status',)
    search_fields = ('name', 'endpoint')
    readonly_fields = ('last_checked',)
