from django.db import models

class Account(models.Model):
    account_number = models.CharField(max_length=12, unique=True)
    aadhar = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='Images')
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    balance = models.FloatField(default=5000.00)
    pin = models.CharField(max_length=20, default=0000)
    address = models.TextField()
    otp = models.IntegerField(null=True, blank=True)  # OTP field for temporary storage

    def __str__(self):
        return self.account_number