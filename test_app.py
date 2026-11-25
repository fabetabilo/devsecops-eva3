from app import create_app

'''
Tres pruebas simples
1. Que `/health` responda
2. Usuario ana / ana123 pueda ingresar
3. Que una contrasena incorrecta sea rechazada
'''

def nuevo_cliente(tmp_path):
    app = create_app(database_path=tmp_path / "test.db")
    app.config["TESTING"] = True
    return app.test_client()


def test_health(tmp_path):
    r = nuevo_cliente(tmp_path).get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_login_correcto(tmp_path):
    cliente = nuevo_cliente(tmp_path)
    r = cliente.post("/login", data={"username": "ana", "password": "ana123"})
    assert r.status_code == 302
    r = cliente.get("/")
    assert "Revisión de despliegue" in r.get_data(as_text=True)


def test_login_incorrecto(tmp_path):
    r = nuevo_cliente(tmp_path).post("/login", data={"username": "ana", "password": "mala"})
    assert "Credenciales inválidas" in r.get_data(as_text=True)
