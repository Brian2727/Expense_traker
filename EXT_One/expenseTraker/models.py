from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

expenses_type = [
    ('grocery','Grocery'),
    ('restaurant','Restaurant'),
    ('gift','Gift'),
    ('electronics','Electronics'),
    ('supplies','Supplies'),
    ('repair','Repair'),
    ('social','Social Life'),
    ('clothing','Clothing'),
    ('cosmetics','Cosmetics'),
    ('medicine','Medicine'),
]
# Create your models here.
class Expense(models.Model):
    name =  models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=100,choices=expenses_type,default="")
    date = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " Cost: " + str(self.amount) + "$ Type of: " + self.category

    def save(self, date=None, *args, **kwargs):
        # Check if the object is being created for the first time

        if not self.pk:
            # Set a custom value for created_at if provided, otherwise use current date and time
            self.date = date or timezone.now()
            print(self.date)
        super().save(*args, **kwargs)

    class Address(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        address = models.CharField(max_length=255)