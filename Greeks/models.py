from django.db import models

class Greeks(models.Model):
    delta = models.IntegerField()
    gamma = models.IntegerField()
    theta = models.IntegerField()
    vega = models.IntegerField()

    def __str__(self):
        return 'delta: ' + str(delta) + ', gamma: ' + str(gamma) + ', theta: ' + str(theta) + 'vega: ' + str(vega)