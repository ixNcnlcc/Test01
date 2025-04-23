from django.db import models
from django.utils import timezone
from django.db import transaction
import random

class Person(models.Model):
    name = models.CharField(max_length=100)
    nisit = models.CharField(max_length=11, unique=True, blank=True)
    degree = models.CharField(max_length=100)
    seat = models.IntegerField(unique=True, blank=True)
    verified = models.IntegerField(default=0, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    rfid = models.CharField(max_length=15, unique=True, blank=True)

    @staticmethod
    def generate_unique_value(length, model, field):
        while True:
            value = ''.join([str(random.randint(0, 9)) for _ in range(length)])
            if not model.objects.filter(**{field: value}).exists():
                return value

    def save(self, *args, **kwargs):
        if not self.nisit:
            self.nisit = self.generate_unique_value(11, Person, 'nisit')
        
        if not self.rfid:
            self.rfid = self.generate_unique_value(15, Person, 'rfid')

        if not self.seat:
            with transaction.atomic():
                # Lock the table to prevent concurrent updates
                last_person = Person.objects.select_for_update().order_by('-seat').first()
                self.seat = last_person.seat + 1 if last_person else 1
        
        super().save(*args, **kwargs)

    def display_id(self):   
        return str(self.id).zfill(4)

    def __str__(self):
        local_date = timezone.localtime(self.date)
        return (
            f"ลำดับ {self.display_id()} "
            f"รหัสนิสิต {self.nisit} "
            f"ชื่อ {self.name} "
            f"อยู่คณะ {self.degree} "
            f"นั่งที่ {self.seat} "
            f"เมื่อ {local_date.strftime('%d/%m/%Y %H:%M:%S')}"
        )