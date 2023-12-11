from datetime import datetime

import pytest

from gasto.models import Segmento, Cardbank, Gasto, Parcelas


@pytest.fixture
def segmento(db):
    return Segmento.objects.create(name="Supermercados")


@pytest.fixture
def cardbank(db):
    return Cardbank.objects.create(name="BB")


@pytest.fixture
def gasto(segmento, cardbank):
    return Gasto.objects.create(
        name="Supermercado Avenida",
        datagasto=datetime.now(),
        segmento=segmento,
        card_bank=cardbank,
    )


@pytest.fixture()
def parcela(gasto):
    return Parcelas.objects.create(
        gasto=gasto, valor_parcela=10.01, data_parcela=datetime.now()
    )
