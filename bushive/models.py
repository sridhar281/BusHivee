from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Operator(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Bus(models.Model):
    bus_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=50)

    def __str__(self):
        return self.bus_number 

class Route(models.Model):
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    distance = models.FloatField()
    estimated_time = models.TimeField()

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"

    
class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Trip on {self.bus} from {self.route.start_location} to {self.route.end_location}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    reservation_status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Reservation for {self.user} on {self.trip}"

class Buspayment(models.Model):
     name=models.CharField(max_length=100)
     amount=models.CharField(max_length=100)
     order_id=models.CharField(max_length=100,blank=True)
     razorpay_payment_id=models.CharField(max_length=100,blank=True)
     paid=models.BooleanField(default=False)
     