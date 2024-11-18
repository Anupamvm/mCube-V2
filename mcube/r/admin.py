from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('trading_symbol', 'instrument_token', 'last_traded_price', 'quote_type', 'timestamp')
    search_fields = ('trading_symbol', 'instrument_token')
    list_filter = ('quote_type', 'exchange_segment')
