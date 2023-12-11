from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from accounts import constants
from accounts.models import Base


class HoraTrabalhada(Base):
    price = models.CharField(verbose_name="Ganho/hora", max_length=100, default=0)
    content = models.TextField(null=True)

    def __str__(self):
        return self.price

    def __repr__(self):
        return str(self.price)

    class Meta:
        verbose_name_plural = "Horas Trabalhadas"
        ordering = ["-id"]


class Rabbiit(Base):
    description = models.CharField(verbose_name="Descrição", max_length=100)
    time_total = models.TimeField(verbose_name="Total de horas", blank=True, null=True)
    time_start = models.TimeField(verbose_name="Hora Inicial", blank=True, null=True)
    time_end = models.TimeField(verbose_name="Hora Final", blank=True, null=True)
    rate_hour = models.ForeignKey(
        HoraTrabalhada,
        verbose_name="Ganho/hora",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    rate_total = models.DecimalField(
        verbose_name="Total Ganho",
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    class Meta:
        verbose_name_plural = "Rabbiits"
        ordering = ["-id"]

    # objects = DataFrameManager()


class City(Base):
    description = models.CharField(verbose_name=_("Description"), max_length=100)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Localidade"
        verbose_name_plural = "Localidades"
        ordering = ["-id"]


class Comercio(Base):
    description = models.CharField(
        verbose_name=_("Description"), max_length=100, unique=True
    )

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    def to_dict(self):
        return {"value": self.pk, "description": self.description}

    class Meta:
        verbose_name = "Comércio"
        verbose_name_plural = "Comércios"
        ordering = ["-id"]


class Pecas(Base):
    data = models.DateField(
        verbose_name=_("Date"),
    )
    veiculo = models.CharField(
        verbose_name=_("Vehicle"), max_length=1, choices=constants.TYPE_VEHICLE
    )
    proxtroca = models.IntegerField(verbose_name=_("Next Exchange"), default=1)
    troca = models.IntegerField(verbose_name=_("change"), default=1)
    comercio = models.ForeignKey(
        Comercio, verbose_name=_("Trade"), on_delete=models.PROTECT
    )
    city = models.ForeignKey(
        City,
        verbose_name=_("Locality"),
        on_delete=models.PROTECT,
        default=1,
        null=True,
        blank=True,
    )
    total = models.CharField(
        verbose_name="Total", blank=True, null=True, max_length=100
    )

    def __str__(self):
        return self.comercio.description

    class Meta:
        verbose_name = "Peça"
        verbose_name_plural = "Peças"
        ordering = ["-id"]


class Itenspecas(models.Model):
    description = models.CharField(verbose_name="Descrição", max_length=100)
    pecas = models.ForeignKey(Pecas, verbose_name="Peças", on_delete=models.PROTECT)
    price = models.CharField(
        verbose_name="Preço", blank=True, null=True, max_length=100
    )
    quantity = models.IntegerField(verbose_name="Quantidade Comprada", default=1)
    subtotal = models.CharField(
        verbose_name="Sub-Total", blank=True, null=True, max_length=100
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Item Peça"
        verbose_name_plural = "Itens Peças"
        ordering = ["-id"]


class Events(Base):
    description = models.CharField(verbose_name="Descrição", max_length=250)
    event_date = models.DateField(verbose_name="Data do Acontecimento")

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    def to_dict(self):
        return {"id": self.id, "description": self.description}

    def get_absolute_url(self):
        return reverse_lazy("website_events_list")

    class Meta:
        verbose_name = "Acontecimento"
        verbose_name_plural = "Acontecimentos"
        ordering = ["-id"]


class Vivo(Base):
    velocity = models.CharField(verbose_name=_("Description"), max_length=250)
    event_date = models.DateField(verbose_name=_("Data Evento"), blank=True, null=True)
    internet_used_in_percentagem = models.CharField(
        verbose_name="Internet Utilizada (%)",
        max_length=10,
        null=True,
        blank=True,
    )
    internet_available_in_percentagem = models.CharField(
        verbose_name="Internet Usada (%)", max_length=10, null=True, blank=True
    )
    internet_used_in_number = models.DecimalField(
        verbose_name="Internet Utilizada",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    internet_available_in_number = models.DecimalField(
        verbose_name="Internet Usada",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    time = models.TimeField()
    price = models.DecimalField(
        verbose_name="Preço",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Vivo"
        verbose_name_plural = "Vivos"


class Planilha(models.Model):
    description = models.CharField(verbose_name="Descrição", max_length=100)
    value = models.DecimalField(
        verbose_name="Valor",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    expenditure_type = models.CharField(
        verbose_name="Tipos de Despesa",
        max_length=1,
        choices=constants.EXPENDITURE_TYPE,
    )
    event_date = models.DateField(verbose_name=_("Data Evento"), null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "value": self.value,
            "expenditure_type": self.expenditure_type,
            "event_date": self.event_date,
        }

    def __str__(self):
        return self.description


class Consultancy(Base):
    name = models.CharField(verbose_name="Nome", max_length=50, unique=True)
    quantity_of_company = models.IntegerField("Quantidade de Empresas", default=0)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Consultoria"
        verbose_name_plural = "Consultorias"
        ordering = ["-id"]


class Empresa(Base):
    name = models.CharField(verbose_name="Nome", max_length=50, unique=True)
    site = models.CharField(max_length=50, default="http://", null=True)
    consulting = models.ForeignKey(
        Consultancy,
        verbose_name="consultorias",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount_applied = models.IntegerField(
        verbose_name="Quantidade aplicada nessa empresa", default=0, null=True
    )
    company_culture = models.TextField(
        verbose_name="Cultura da Empresa", null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Skill(Base):
    description = models.CharField("Descrição", max_length=30, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Habilidade"
        ordering = ["-id"]


class Emprego(Base):
    company = models.ForeignKey(
        Empresa,
        verbose_name="Empresa",
        on_delete=models.CASCADE,
    )
    entrade_date = models.DateField(verbose_name="Data de Entrada")
    job = models.CharField(verbose_name="Vaga", max_length=50, null=True)
    requisite = models.TextField(verbose_name="Requisitos", null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    feedback = models.CharField(
        max_length=100, help_text="ex. Outro Candidato", null=True, blank=True
    )
    feedback_date = models.DateField(
        verbose_name="Data do feedback", null=True, blank=True
    )
    process_fase = models.CharField(
        verbose_name="Etapa do processo",
        max_length=20,
        choices=constants.TYPE_PROCCESS_FASE,
        default=constants.CADASTRO,
    )
    vacancy_found = models.CharField(
        verbose_name="Vaga encontrada em",
        max_length=2,
        choices=constants.TYPE_VACANCY_FOUND,
        default=constants.OUTRO,
    )
    count_day_contact = models.IntegerField(verbose_name="Dias passados", default=0)

    def __str__(self):
        return f"Vaga: {self.job} na empresa: {self.company.name}"

    class Meta:
        ordering = ["entrade_date"]

    def display_skills(self):
        """Create a string for the Skills. This is required to display skills in Admin."""
        return ", ".join(skill.description for skill in self.skills.all())

    display_skills.short_description = "Skills"
