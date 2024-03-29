from datetime import datetime


def test_segmento(segmento):
    assert "Supermercados" in segmento.name


def test_card_bank(cardbank):
    assert "BB" in cardbank.name


def test_gasto(gasto):
    assert gasto.name == "Supermercado Avenida"


def test_parcelas(parcela):
    assert parcela.parcelas == 1
    assert parcela.valor_parcela == 10.01
    assert parcela.data_parcela.date() == datetime.now().date()
    assert parcela.numero_parcela == 1
    assert parcela.gasto.name == "Supermercado Avenida"
