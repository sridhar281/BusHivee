from django.contrib import admin
from .models import User, Operator, Bus, Route, Trip, Reservation, Buspayment

admin.site.register(User)
admin.site.register(Operator)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Reservation)
admin.site.register(Buspayment)
