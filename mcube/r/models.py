from django.db import models
from django.utils.timezone import now

class Quote(models.Model):
    # Enum for type field
    class QuoteType(models.TextChoices):
        INDEX = "index", "Index"
        EQUITY = "equity", "Equity"
        FUTURES = "futures", "Futures"
        CALL_OPTIONS = "calloptions", "Call Options"
        PUT_OPTIONS = "putoptions", "Put Options"

    # General stock information
    last_traded_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_traded_quantity = models.IntegerField()
    lower_circuit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    upper_circuit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    week_52_high = models.DecimalField(max_digits=10, decimal_places=2)
    week_52_low = models.DecimalField(max_digits=10, decimal_places=2)
    multiplier = models.IntegerField()
    precision = models.IntegerField()
    change = models.DecimalField(max_digits=10, decimal_places=2)
    net_change_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    # Identifiers and metadata
    instrument_token = models.CharField(max_length=20)
    exchange_segment = models.CharField(max_length=10)
    trading_symbol = models.CharField(max_length=50)
    request_type = models.CharField(max_length=20)

    # OHLC data
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Type of quote (e.g., Index, Equity, Futures, etc.)
    quote_type = models.CharField(
        max_length=20,
        choices=QuoteType.choices,
        default=QuoteType.EQUITY
    )

    # Timestamp for when the quote was saved
    timestamp = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.trading_symbol} ({self.instrument_token}) - {self.last_traded_price} [{self.quote_type}]"
