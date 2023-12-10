
def test_autocomplete_gasto(client, gasto):
    resp = client.get(
        "/gasto/autocomplete/?term=Avenida",
    )
    assert resp.status_code == 200
    assert isinstance(resp.content, bytes)
    assert 'Supermercado Avenida' in resp.content.decode('utf-8')


def test_autocomplete_gasto_retorno_vazio(client, gasto):
    resp = client.get(
        "/gasto/autocomplete/?term=Venceslau",
    )
    assert resp.status_code == 200
    assert '' in resp.content.decode('utf-8')
