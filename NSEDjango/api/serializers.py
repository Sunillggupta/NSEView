"""
Django REST Framework serializers for NSE data
"""
from rest_framework import serializers
from .models import Index, IndexHistory, APIStatus

class IndexSerializer(serializers.ModelSerializer):
    """Serializer for Index model"""
    class Meta:
        model = Index
        fields = [
            'id', 'name', 'symbol', 'key',
            'last_price', 'open_price', 'high_price', 'low_price', 'previous_close',
            'change', 'percent_change',
            'year_high', 'year_low',
            'pe_ratio', 'pb_ratio', 'dividend_yield',
            'advances', 'declines', 'unchanged',
            'change_30d', 'change_365d',
            'last_updated', 'created_at'
        ]
        read_only_fields = ['id', 'last_updated', 'created_at']


class IndexHistorySerializer(serializers.ModelSerializer):
    """Serializer for IndexHistory model"""
    index_name = serializers.CharField(source='index.name', read_only=True)
    
    class Meta:
        model = IndexHistory
        fields = ['id', 'index', 'index_name', 'timestamp', 'price', 'change', 'percent_change']
        read_only_fields = ['id', 'timestamp']


class APIStatusSerializer(serializers.ModelSerializer):
    """Serializer for APIStatus model"""
    class Meta:
        model = APIStatus
        fields = ['id', 'name', 'endpoint', 'status', 'message', 'last_checked']
        read_only_fields = ['id', 'last_checked']


class IndexListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for index listing (fields the dashboard table needs)"""
    class Meta:
        model = Index
        fields = [
            'id', 'name', 'symbol', 'key',
            'last_price', 'change', 'percent_change',
            'open_price', 'high_price', 'low_price', 'previous_close',
            'pe_ratio',
        ]


class IndexDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with all fields"""
    history = IndexHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Index
        fields = '__all__'
