from accounts.models import User

def test_criar_user(db):
    User.objects.create(
        username='teste',
        password='mudar1234',
        email='zicadopv@gmail.com',
        is_superuser=True
    )
    assert User.objects.count() == 1
    user = User.objects.filter(id=1).values()
    assert list(user)[0]['username'] == 'teste'
    assert list(user)[0]['email'] == 'zicadopv@gmail.com'
