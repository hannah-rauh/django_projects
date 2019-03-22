from django.db import models

class Category(models.Model) :
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name

class iso(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name


class States(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name



class Site(models.Model):
    name = models.CharField(max_length=128)
    year = models.IntegerField(null=True)
    description=models.CharField(max_length=128)
    justification=models.CharField(max_length=128)
    longitude=models.FloatField(null=True)
    latitude=models.FloatField(null=True)
    area_hectares=models.FloatField(null=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    iso = models.ForeignKey(iso, on_delete=models.CASCADE,null=True,blank=True)
    states=models.ForeignKey(States, on_delete=models.CASCADE,null=True,blank=True)
    region= models.ForeignKey(Region, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self) :
        return self.name #return more selfs
