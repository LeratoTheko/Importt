from django.db import models

class Alums(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
