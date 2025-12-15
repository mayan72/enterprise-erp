from django.db import models

# Create your models here.
class ERPModule(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, default="layers")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
