TYPE_VEHICLE = (
    ("C", "Carro"),
    ("M", "Moto"),
)

EXPENDITURE_TYPE = (
    ("F", "FIXAS"),
    ("V", "VARIÁVEIS"),
)

CADASTRO = "Cadastro"
TYPE_PROCCESS_FASE = (
    (CADASTRO, "Cadastro"),
    ("Inicial", "Bate-papo Inicial"),
    ("Teste", "Teste Técnico"),
    ("Entrevista", "Entrevista"),
    ("Finalizada", "Finalizada"),
)


OUTRO = "ou"
TYPE_VACANCY_FOUND = (
    (OUTRO, "Outro"),
    ("li", "Linkedin"),
    ("fb", "Facebook"),
    ("te", "Telegram"),
    ("co", "Coodesh"),
    ("gr", "Gupy"),
    ("vg", "Vagas"),
)


INATIVO, ATIVO = False, True
STATUS = (
    (ATIVO, "Ativa"),
    (INATIVO, "Inativa"),
)

NAO, SIM = 0, 1
OBRIGATORIO = (
    (NAO, "Não"),
    (SIM, "Sim"),
)

MASCULINO, FEMININO, INDEFINIDO = "M", "F", "I"
SEXO = (
    (MASCULINO, "MASCULINO"),
    (FEMININO, "FEMININO"),
    (INDEFINIDO, "INDEFINIDO"),
)

MESES = {
    0: "",
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

CREDITO, DEBITO, TRANSFERENCIA = "C", "D", "T"
CARTAO = (
    (CREDITO, "Crédito"),
    (DEBITO, "Débito"),
    (TRANSFERENCIA, "Transferência"),
)
