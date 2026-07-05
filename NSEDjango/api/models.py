"""
Django models for NSE data
"""
from django.db import models
from django.utils import timezone

class Index(models.Model):
    """Model for NSE indices"""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    symbol = models.CharField(max_length=50, unique=True, db_index=True)
    key = models.CharField(max_length=100)  # Category: DERIVATIVES, BROAD MARKET, etc.
    
    # Price data
    last_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    open_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    high_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    low_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    previous_close = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Changes
    change = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    percent_change = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # 52-week data
    year_high = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    year_low = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Valuation metrics
    pe_ratio = models.CharField(max_length=20, null=True, blank=True)
    pb_ratio = models.CharField(max_length=20, null=True, blank=True)
    dividend_yield = models.CharField(max_length=20, null=True, blank=True)
    
    # Market activity
    advances = models.IntegerField(null=True, blank=True)
    declines = models.IntegerField(null=True, blank=True)
    unchanged = models.IntegerField(null=True, blank=True)
    
    # Performance
    change_30d = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    change_365d = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Index'
        verbose_name_plural = 'Indices'
    
    def __str__(self):
        return f"{self.name} ({self.last_price})"


class IndexHistory(models.Model):
    """Model for storing historical index data"""
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Price at this time
    price = models.DecimalField(max_digits=12, decimal_places=2)
    change = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    percent_change = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Index Histories'
    
    def __str__(self):
        return f"{self.index.name} @ {self.timestamp}: {self.price}"


class APIStatus(models.Model):
    """Model for API status tracking"""
    name = models.CharField(max_length=100, unique=True)
    endpoint = models.URLField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('working', 'Working'),
            ('blocked', 'Blocked'),
            ('error', 'Error'),
            ('unknown', 'Unknown'),
        ],
        default='unknown'
    )
    message = models.TextField(blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}: {self.status}"
    
    class Meta:
        verbose_name_plural = 'API Statuses'

