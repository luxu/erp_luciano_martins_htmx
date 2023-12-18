from django.db import models

from accounts.models import Base


class Events(Base):
    description = models.CharField(verbose_name="Descrição", max_length=250)
    event_date = models.DateField(verbose_name="Data do Acontecimento")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Acontecimento"
        verbose_name_plural = "Acontecimentos"
        ordering = ["-id"]
