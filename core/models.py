from django.db import models


class Theme(models.Model):
    color = models.CharField(max_length=1000)
    user = models.CharField(max_length=1000)

    def __str__(self):
        return self.user


class Setting(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.name
