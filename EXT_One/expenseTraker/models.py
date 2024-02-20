from django.db import models

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
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name + " Cost: " + str(self.amount) + "$ Type of: " + self.category