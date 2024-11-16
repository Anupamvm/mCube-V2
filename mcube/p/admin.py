from django.contrib import admin
from .models import Holding


# Register your models here.
@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'quantity', 'market_value', 'expiry_date')  # Customize fields to display