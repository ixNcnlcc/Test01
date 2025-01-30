from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    nisit = models.IntegerField(default=1, blank=True)
    degree = models.CharField(max_length=100)
    seat = models.IntegerField(default=1, blank=True)
    verified = models.IntegerField(default=0, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def display_id(self):
        return str(self.id).zfill(4)

    def __str__(self):
        local_date = timezone.localtime(self.date)
        return (
            f"ลำดับ {str(self.id).zfill(4)} "
            f"รหัสนิสิต {str(self.nisit).zfill(11)} "
            f"ชื่อ {self.name} "
            f"อยู่คณะ {self.degree} "
            f"นั่งที่ {self.seat} "
            f"เมื่อ {local_date.strftime('%d/%m/%Y %H:%M:%S')}"
        )
