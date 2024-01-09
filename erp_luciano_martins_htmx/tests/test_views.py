from http import HTTPStatus

from accounts.models import User


def test_home_apos_logar(client, db, admin_client):
    user = User.objects.create(
        username="teste",
        password="mudar1234",
        email="zicadopv@gmail.com",
        is_superuser=True,
    )
    client.force_login(user)
    client.get("/")
    response = admin_client.get("/")
    assert response.status_code == HTTPStatus.OK
