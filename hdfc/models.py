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
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer', 'Transfer'),
    ]
    sender_account = models.CharField(max_length=20, null=True, blank=True)
    receiver_account = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - ₹{self.amount} on {self.date.strftime('%d-%m-%Y')}"
