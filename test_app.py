from app import create_app


def nuevo_cliente(tmp_path):
    app = create_app(database_path=tmp_path / "test.db")
    app.config["TESTING"] = True
    return app.test_client()


def cliente_autenticado(tmp_path):
    cliente = nuevo_cliente(tmp_path)
    cliente.post("/login", data={"username": "ana", "password": "ana123"})
    return cliente


def test_health(tmp_path):
    r = nuevo_cliente(tmp_path).get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_login_correcto(tmp_path):
    cliente = nuevo_cliente(tmp_path)
    r = cliente.post("/login", data={"username": "ana", "password": "ana123"})
    assert r.status_code == 302


def test_login_incorrecto(tmp_path):
    r = nuevo_cliente(tmp_path).post("/login", data={"username": "ana", "password": "mala"})
    assert "Credenciales inválidas" in r.get_data(as_text=True)


# --- Revision de seguridad: inyección SQL en /search ---
# estos dos tests fallan con el codigo (identifican el fallo en el pipeline) y pasan al parametrizar 
# la consulta en /search

def test_busqueda_no_filtra_credenciales(tmp_path):
    """La búsqueda NO debe permitir leer la tabla de usuarios (inyección UNION)."""
    cliente = cliente_autenticado(tmp_path)
    payload = "' UNION SELECT id, username || ':' || password_hash FROM users -- "
    r = cliente.get("/search", query_string={"q": payload})
    assert "pbkdf2:" not in r.get_data(as_text=True), "Inyección SQL: se filtraron hashes de contraseña"


def test_busqueda_no_permite_inyeccion(tmp_path):
    """Un texto con comilla no debe romper la consulta ni devolver todo con 'OR 1=1'."""
    cliente = cliente_autenticado(tmp_path)
    r = cliente.get("/search", query_string={"q": "' OR 1=1 -- "})
    assert r.status_code == 200
    # con la consulta parametrizada, este texto se busca literal y no encuentra nada
    assert "Acceso al panel" not in r.get_data(as_text=True)
