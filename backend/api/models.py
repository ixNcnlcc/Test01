from django.db import models
from django.utils import timezone
import random

class Person(models.Model):
    name = models.CharField(max_length=100)
    nisit = models.CharField(max_length=11, unique=True, blank=True)
    degree = models.CharField(max_length=100)
    seat = models.IntegerField(unique=True, blank=True)
    verified = models.IntegerField(default=0, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    rfid = models.CharField(max_length=15, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # สร้างรหัสนิสิต (nisit) สุ่ม 11 หลัก หากยังไม่มี
        if not self.nisit:
            self.nisit = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        
        # สร้าง RFID สุ่ม 15 หลัก หากยังไม่มี
        if not self.rfid:
            self.rfid = ''.join([str(random.randint(0, 9)) for _ in range(15)])
        
        # กำหนดค่า seat หากยังไม่มี
        if not self.seat:
            last_person = Person.objects.order_by('-seat').first()
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