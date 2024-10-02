from django.db import models

class Market(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    text = models.TextField(null=True, blank=True)
    score = models.IntegerField()

    def __str__(self):
        return f'Review for {self.market.name} by {self.username}'