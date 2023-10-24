from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Shipment(models.Model):

    CHOICES = (
        ('P', 'Pending'),
        ('A', 'Assigned'),
        ('PU', 'picked up'),
        ('D', 'delivered'),
        ('C', 'cancelled')
    )
    
    name = models.CharField(max_length=255, blank=False, null=False)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pick_up_location = models.CharField(max_length=255, blank=False, null=False)
    drop_off_location = models.CharField(max_length=255, blank=False, null=False)
    delivery_instructions = models.TextField()
    estimated_time = models.CharField(max_length=100, blank=False, null=False)
    total_cost = models.CharField(max_length=50, blank=False, null=False)
    items = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=2, choices=CHOICES, default='P')
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name) + ' - ' + str(self.status)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'

