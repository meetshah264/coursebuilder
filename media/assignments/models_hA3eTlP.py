from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CarType(models.Model):
  name = models.CharField(max_length=150)
  def __str__(self):
    return self.name

class Vehicle(models.Model):
  car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
  car_name = models.CharField(max_length=200)
  car_price = models.DecimalField(max_digits=10, decimal_places=4)
  inventory = models.PositiveIntegerField(default=10)
  instock = models.BooleanField(default=True)
  product_description = models.CharField(max_length=300, blank=True, null=True)
  CAR_FEATURES = [
    ('Cruise Control','Cruise Control'),
    ('Audio Interface','Audio Interface'),
    ('Airbags','Airbags'),
    ('Air Conditioning','Air Conditioning'),
    ('Seat Heating','Seat Heating'),
    ('ParkAssist','ParkAssist'),
    ('Power Steering','Power Steering'),
    ('Reversing Camera','Reversing Camera'),
    ('Auto Start/Stop','Auto Start/Stop'),
  ]
  car_features= models.CharField(max_length=300, choices=CAR_FEATURES, default='Airbags')

  def __str__(self):
    return self.car_name
  
class Buyer(User):
  AREA_CHOICES = [
    ('W','Windsor'),
    ('WA','Waterloo'),
    ('T','Toronto'),
    ('C', 'Chatham'),
    ('LS', 'LaSalle'),
    ('A', 'Amherstburg'),
    ('L', 'Lakeshore'),
    ('LE', 'Leamington'),]
  shipping_address = models.CharField(max_length=300, null=True, blank=True)
  area=models.CharField(max_length=2, choices=AREA_CHOICES, default='C')
  interested_in = models.ManyToManyField(CarType)
  phone = PhoneNumberField(null=True)
  fullname = models.CharField(max_length=30, null=True)
  def __str__(self):
    return self.fullname

class OrderVehicle(models.Model):
  vehicle_id = models.ForeignKey(Vehicle, related_name='order_vehicle', on_delete=models.CASCADE)
  buyer_id = models.ForeignKey(Buyer, related_name='order_vehicle_buyer', on_delete=models.CASCADE)
  number_order_vehicle = models.PositiveIntegerField(default=0)
  STATUS_OF_ORDER = [
    ('0','Cancelled Order'),
    ('1','Placed Order'),
    ('2','Shipped Order'),
    ('3','Delivered Order'),
  ]
  status=models.CharField(max_length=1, choices=STATUS_OF_ORDER, default='A')
  last_updated = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.status
  
  def get_total_price_for_order(self):
    total_price = 0
    order_vehicles = self.objects.values_list('number_order_vehicle', flat=True)
    for order_vehicle in order_vehicles:
      total_price += order_vehicle.total_price()
    return total_price

class Description(models.Model):
  TITLE_CHOICES = [
        ('carsite', 'A carsite website for the buyers'),
        ('ecommerce', 'An ecommerce platform for online shopping'),
        ('blog', 'A blog website for sharing articles'),]
  titles = models.CharField(max_length=100, choices=TITLE_CHOICES)
  text = models.TextField()
  new_description_added = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.titles

class Project(models.Model):
  descriptions = models.ManyToManyField(Description)

class MembersName(models.Model):
  first_name = models.CharField(max_length=50, null=False)
  last_name = models.CharField(max_length=50, null=False)
  semester = models.PositiveIntegerField(default=3)
  link = models.URLField()

  def __str__(self):
    return self.first_name

  class Meta:
    ordering = ['first_name']
