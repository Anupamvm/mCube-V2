from django.db import models

class Holding(models.Model):
    display_symbol = models.CharField(max_length=100)
    average_price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    exchange_segment = models.CharField(max_length=50, null=True, blank=True)
    exchange_identifier = models.CharField(max_length=50, null=True, blank=True)
    holding_cost = models.FloatField(null=True, blank=True)
    market_value = models.FloatField(null=True, blank=True)
    scrip_id = models.CharField(max_length=64, null=True, blank=True)  # Changed to CharField
    instrument_token = models.IntegerField(null=True, blank=True)
    instrument_type = models.CharField(max_length=50, null=True, blank=True)
    is_alternate_scrip = models.BooleanField(null=True, blank=True)
    closing_price = models.FloatField(null=True, blank=True)
    symbol = models.CharField(max_length=100)
    sellable_quantity = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    strike_price = models.FloatField(null=True, blank=True)
    opt_type = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.display_symbol} ({self.symbol})"
