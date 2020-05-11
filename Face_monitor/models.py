from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    pub_date = models.DateField()
    # publish = models.ForeignKey