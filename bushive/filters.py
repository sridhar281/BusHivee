import django_filters
from .models import Route,Reservation,Trip

class busFilter(django_filters.FilterSet):
    class Meta:
        model= Route
        fields='__all__'
        
class checkFilter(django_filters.FilterSet):
    class Meta:
        model=Reservation
        fields='__all__'
        
class OrderFilter(django_filters.FilterSet):
    class Meta:
             model=Trip
             fields='__all__' 