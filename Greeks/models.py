from django.db import models

class Greeks(models.Model):
    delta = models.DecimalField(decimal_places=10, max_digits=20)
    gamma = models.DecimalField(decimal_places=10, max_digits=20)
    theta = models.DecimalField(decimal_places=10, max_digits=20)
    vega = models.DecimalField(decimal_places=10, max_digits=20)
    error = models.CharField(max_length=30)
    def __str__(self):
        return 'delta: ' + str(delta) + ', gamma: ' + str(gamma) + ', theta: ' + str(theta) + 'vega: ' + str(vega)