# Generated by Django 4.2.7 on 2023-11-18 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cardbank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="Nome")),
            ],
            options={
                "verbose_name": "Banco do cartão",
                "verbose_name_plural": "Bancos do cartão",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="Description"),
                ),
            ],
            options={
                "verbose_name": "Localidade",
                "verbose_name_plural": "Localidades",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Comercio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Description"
                    ),
                ),
            ],
            options={
                "verbose_name": "Comércio",
                "verbose_name_plural": "Comércios",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Consultancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=50, unique=True, verbose_name="Nome"),
                ),
                (
                    "quantity_of_company",
                    models.IntegerField(
                        default=0, verbose_name="Quantidade de Empresas"
                    ),
                ),
            ],
            options={
                "verbose_name": "Consultoria",
                "verbose_name_plural": "Consultorias",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Events",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=250, verbose_name="Descrição"),
                ),
                ("event_date", models.DateField(verbose_name="Data do Acontecimento")),
            ],
            options={
                "verbose_name": "Acontecimento",
                "verbose_name_plural": "Acontecimentos",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Gasto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="nome")),
                (
                    "more_infos",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Infos Complementares",
                    ),
                ),
                ("datagasto", models.DateField(verbose_name="Data do Gasto")),
                (
                    "total",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Valor Total",
                    ),
                ),
                (
                    "description_on_invoice",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Descrição na fatura",
                    ),
                ),
                (
                    "opcoes_cartao",
                    models.CharField(
                        choices=[
                            ("C", "Crédito"),
                            ("D", "Débito"),
                            ("T", "Transferência"),
                        ],
                        default="C",
                        max_length=1,
                        verbose_name="Tipo de pagamento",
                    ),
                ),
                (
                    "card_bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cardbanks",
                        to="website.cardbank",
                        verbose_name="Banco do cartão",
                    ),
                ),
            ],
            options={
                "verbose_name": "Gasto",
                "verbose_name_plural": "Gastos",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="HoraTrabalhada",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "price",
                    models.CharField(
                        default=0, max_length=100, verbose_name="Ganho/hora"
                    ),
                ),
                ("content", models.TextField(null=True)),
            ],
            options={
                "verbose_name_plural": "Horas Trabalhadas",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Planilha",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="Descrição"),
                ),
                (
                    "value",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=3,
                        null=True,
                        verbose_name="Valor",
                    ),
                ),
                (
                    "expenditure_type",
                    models.CharField(
                        choices=[("F", "FIXAS"), ("V", "VARIÁVEIS")],
                        max_length=1,
                        verbose_name="Tipos de Despesa",
                    ),
                ),
                ("event_date", models.DateField(null=True, verbose_name="Data Evento")),
            ],
        ),
        migrations.CreateModel(
            name="Segmento",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Tipo de comércio"),
                ),
            ],
            options={
                "verbose_name": "Segmento do Comercio",
                "verbose_name_plural": "Segmentos do Comercio",
                "ordering": ["-name"],
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=30, null=True, verbose_name="Descrição"
                    ),
                ),
            ],
            options={
                "verbose_name": "Habilidade",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Vivo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "velocity",
                    models.CharField(max_length=250, verbose_name="Description"),
                ),
                (
                    "event_date",
                    models.DateField(blank=True, null=True, verbose_name="Data Evento"),
                ),
                (
                    "internet_used_in_percentagem",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Internet Utilizada (%)",
                    ),
                ),
                (
                    "internet_available_in_percentagem",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Internet Usada (%)",
                    ),
                ),
                (
                    "internet_used_in_number",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=3,
                        null=True,
                        verbose_name="Internet Utilizada",
                    ),
                ),
                (
                    "internet_available_in_number",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=3,
                        null=True,
                        verbose_name="Internet Usada",
                    ),
                ),
                ("time", models.TimeField()),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=3,
                        null=True,
                        verbose_name="Preço",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vivo",
                "verbose_name_plural": "Vivos",
            },
        ),
        migrations.CreateModel(
            name="Rabbiit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="Descrição"),
                ),
                (
                    "time_total",
                    models.TimeField(
                        blank=True, null=True, verbose_name="Total de horas"
                    ),
                ),
                (
                    "time_start",
                    models.TimeField(
                        blank=True, null=True, verbose_name="Hora Inicial"
                    ),
                ),
                (
                    "time_end",
                    models.TimeField(blank=True, null=True, verbose_name="Hora Final"),
                ),
                (
                    "rate_total",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=6,
                        null=True,
                        verbose_name="Total Ganho",
                    ),
                ),
                (
                    "rate_hour",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="website.horatrabalhada",
                        verbose_name="Ganho/hora",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Rabbiits",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Pecas",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                ("data", models.DateField(verbose_name="Date")),
                (
                    "veiculo",
                    models.CharField(
                        choices=[("C", "Carro"), ("M", "Moto")],
                        max_length=1,
                        verbose_name="Vehicle",
                    ),
                ),
                (
                    "proxtroca",
                    models.IntegerField(default=1, verbose_name="Next Exchange"),
                ),
                ("troca", models.IntegerField(default=1, verbose_name="change")),
                (
                    "total",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Total"
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        default=1,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="website.city",
                        verbose_name="Locality",
                    ),
                ),
                (
                    "comercio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="website.comercio",
                        verbose_name="Trade",
                    ),
                ),
            ],
            options={
                "verbose_name": "Peça",
                "verbose_name_plural": "Peças",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Parcelas",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "parcelas",
                    models.IntegerField(default=1, verbose_name="Total de parcelas"),
                ),
                (
                    "numero_parcela",
                    models.IntegerField(default=1, verbose_name="Número da parcela"),
                ),
                (
                    "valor_parcela",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Valor da Parcela",
                    ),
                ),
                (
                    "data_parcela",
                    models.DateField(
                        blank=True, null=True, verbose_name="Installment Date"
                    ),
                ),
                (
                    "gasto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parcelas_gasto",
                        to="website.gasto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Parcela do gasto",
                "verbose_name_plural": "Parcelas dos gasto",
            },
        ),
        migrations.CreateModel(
            name="Itenspecas",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="Descrição"),
                ),
                (
                    "price",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Preço"
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(default=1, verbose_name="Quantidade Comprada"),
                ),
                (
                    "subtotal",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Sub-Total"
                    ),
                ),
                (
                    "pecas",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="website.pecas",
                        verbose_name="Peças",
                    ),
                ),
            ],
            options={
                "verbose_name": "Item Peça",
                "verbose_name_plural": "Itens Peças",
                "ordering": ["-id"],
            },
        ),
        migrations.AddField(
            model_name="gasto",
            name="segmento",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="segmento",
                to="website.segmento",
            ),
        ),
        migrations.CreateModel(
            name="Empresa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=50, unique=True, verbose_name="Nome"),
                ),
                ("site", models.CharField(default="http://", max_length=50, null=True)),
                (
                    "amount_applied",
                    models.IntegerField(
                        default=0,
                        null=True,
                        verbose_name="Quantidade aplicada nessa empresa",
                    ),
                ),
                (
                    "company_culture",
                    models.TextField(
                        blank=True, null=True, verbose_name="Cultura da Empresa"
                    ),
                ),
                (
                    "consulting",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="website.consultancy",
                        verbose_name="consultorias",
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Emprego",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[(True, "Ativa"), (False, "Inativa")], default=True
                    ),
                ),
                ("entrade_date", models.DateField(verbose_name="Data de Entrada")),
                (
                    "job",
                    models.CharField(max_length=50, null=True, verbose_name="Vaga"),
                ),
                (
                    "requisite",
                    models.TextField(blank=True, null=True, verbose_name="Requisitos"),
                ),
                (
                    "feedback",
                    models.CharField(
                        blank=True,
                        help_text="ex. Outro Candidato",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "feedback_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Data do feedback"
                    ),
                ),
                (
                    "process_fase",
                    models.CharField(
                        choices=[
                            ("Cadastro", "Cadastro"),
                            ("Inicial", "Bate-papo Inicial"),
                            ("Teste", "Teste Técnico"),
                            ("Entrevista", "Entrevista"),
                            ("Finalizada", "Finalizada"),
                        ],
                        default="Cadastro",
                        max_length=20,
                        verbose_name="Etapa do processo",
                    ),
                ),
                (
                    "vacancy_found",
                    models.CharField(
                        choices=[
                            ("ou", "Outro"),
                            ("li", "Linkedin"),
                            ("fb", "Facebook"),
                            ("te", "Telegram"),
                            ("co", "Coodesh"),
                            ("gr", "Gupy"),
                            ("vg", "Vagas"),
                        ],
                        default="ou",
                        max_length=2,
                        verbose_name="Vaga encontrada em",
                    ),
                ),
                (
                    "count_day_contact",
                    models.IntegerField(default=0, verbose_name="Dias passados"),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.empresa",
                        verbose_name="Empresa",
                    ),
                ),
                ("skills", models.ManyToManyField(blank=True, to="website.skill")),
            ],
            options={
                "ordering": ["entrade_date"],
            },
        ),
    ]
