from django.db import models

# Create your models here.

class Shipment(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    quatity = models.IntegerField()
    tracking_info = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name) + ' ' + str(self.quatity)
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'