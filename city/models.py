from django.db import models

from accounts.models import Base


class City(Base):
    description = models.CharField(verbose_name="Description", max_length=100)

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    class Meta:
        verbose_name = "Localidade"
        verbose_name_plural = "Localidades"
        ordering = ["-id"]
        db_table = "website_city"
