"""
Django REST Framework views for NSE API
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Index, IndexHistory, APIStatus
from .serializers import (
    IndexSerializer, IndexListSerializer, IndexDetailSerializer,
    IndexHistorySerializer, APIStatusSerializer
)
from .services import sync_indices
from NSEView.NSEDjango.nse_data import NSEDataFetcher

class IndexViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for handling Index data
    Provides list, retrieve, and custom actions
    """
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    lookup_field = 'symbol'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'symbol', 'key']
    ordering_fields = ['name', 'last_price', 'percent_change']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list, detailed for retrieve"""
        if self.action == 'list':
            return IndexListSerializer
        elif self.action == 'retrieve':
            return IndexDetailSerializer
        return IndexSerializer
    
    @action(detail=False, methods=['get'])
    def refresh(self, request):
        """
        Refresh all indices data from NSE API
        GET /api/indices/refresh/
        """
        try:
            result = sync_indices(record_history=True)
            return Response({
                'status': 'success',
                'message': (
                    f"Synced {result['created'] + result['updated']} indices "
                    f"({result['created']} new, {result['updated']} updated)"
                ),
                'created': result['created'],
                'updated': result['updated'],
                'total': result['total'],
                'timestamp': result['timestamp'],
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def history(self, request, symbol=None):
        """
        Get historical data for a specific index
        GET /api/indices/{symbol}/history/
        """
        try:
            index = self.get_object()
            history = IndexHistory.objects.filter(index=index).order_by('-timestamp')[:100]
            serializer = IndexHistorySerializer(history, many=True)
            return Response(serializer.data)
        except Index.DoesNotExist:
            return Response(
                {'error': 'Index not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class IndexHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for handling historical index data"""
    queryset = IndexHistory.objects.all()
    serializer_class = IndexHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['index']
    ordering = ['-timestamp']


class APIStatusViewSet(viewsets.ViewSet):
    """ViewSet for API status information"""
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        """
        Get overall API status
        GET /api/status/
        """
        try:
            fetcher = NSEDataFetcher()
            all_data = fetcher.get_all_indices()
            
            return Response({
                'status': 'operational',
                'message': 'NSE Data API is operational',
                'endpoints': {
                    'allIndices': 'working',
                    'quote-equity': 'blocked (NSE has restricted access)'
                },
                'available_indices': len(all_data.get('data', [])),
                'timestamp': all_data.get('timestamp'),
                'note': 'Individual equity quotes are not available (API blocked)'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Health check endpoint
        GET /api/health/
        """
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'api': 'responding'
        })

