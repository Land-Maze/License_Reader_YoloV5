from django.db import models

# Create your models here.

class License(models.Model):
    license_number = models.CharField(max_length=100, blank=True, primary_key=True)
    last_seen = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_number
    
    
class License_Detect(models.Model):
    id = models.AutoField(primary_key=True)
    license_number = models.ForeignKey(License, on_delete=models.CASCADE, unique=False)
    in_out = models.CharField(max_length=3, blank=False)
    camera_feed_id = models.IntegerField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.license_number} - {self.in_out} - {self.camera_feed_id} - {self.created}"