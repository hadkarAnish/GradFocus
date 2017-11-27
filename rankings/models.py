from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse


class City(models.Model):
    name = models.CharField(max_length=50)
    livingExpense = models.PositiveIntegerField()
    minTemperature = models.FloatField()
    maxTemperature = models.FloatField()
    logo = models.FileField(default=None)

    def get_absolute_url(self):
        # the return below states that go to this view,keyWord args: use the primary key of the current crated object,
        #  and go to dtail using this pk
        return reverse('rankings:details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class University(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    logo = models.FileField()
    isFavourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('rankings:details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s, ID is %i" % (self.name, self.id)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"
