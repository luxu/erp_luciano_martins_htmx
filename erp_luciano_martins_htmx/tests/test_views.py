from http import HTTPStatus

from django.urls import reverse_lazy

from accounts.models import User


def test_home_apos_logar(client, db, admin_client):
    user = User.objects.create(
        username='teste',
        password='mudar1234',
        email='zicadopv@gmail.com',
        is_superuser=True
    )
    client.force_login(user)
    client.get(reverse_lazy("accounts:index"))
    url = reverse_lazy("accounts:index")
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
