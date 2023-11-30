from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts import constants


class Base(models.Model):
    """Base parent model for all the models"""
    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
        null=True
    )
    modified_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
        null=True
    )
    status = models.BooleanField(
        choices=constants.STATUS,
        default=constants.ATIVO
    )

    class Meta:
        abstract = True

class User(AbstractUser):
    username = models.CharField(
        "Usuário",
        max_length=30,
        unique=True,
    )
    name = models.CharField("Nome", max_length=100, blank=True)
    first_name = models.CharField("Primeiro Nome", max_length=150, blank=True)
    last_name = models.CharField("Último Nome", max_length=150, blank=True)
    email = models.EmailField("E-mail", unique=True)
    is_staff = models.BooleanField("Equipe", default=False)
    is_active = models.BooleanField("Ativo", default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.name or self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "accounts_user"

