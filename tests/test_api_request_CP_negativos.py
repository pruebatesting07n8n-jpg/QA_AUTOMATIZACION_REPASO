import pytest


# ==========================================
# 1. MÉTODOS GET
# ==========================================

def test_get_inexistente_estatus(api_session, base_url):
    """
    Valida que al solicitar un recurso inexistente:
    - Retorne un código de estado 404.
    - El cuerpo de la respuesta sea un objeto vacío.
    """
    response = api_session.get(f"{base_url}/posts/999")
    assert response.status_code == 404, f"Se esperaba 404, se obtuvo {response.status_code}"
    assert response.json() == {}, "El cuerpo de respuesta debe estar vacío"


def test_get_listado_estatus(api_session, base_url):
    """
    Verifica que la consulta general del recurso no devuelva errores
    de la familia 4xx (cliente) o 5xx (servidor).
    """
    response = api_session.get(f"{base_url}/posts/")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    assert not (400 <= response.status_code < 600), "La petición retornó un error 4xx o 5xx"


def test_get_fuerza_error_500(api_session, base_url):
    """
    Valida el manejo de caracteres no permitidos en la URI.
    Garantiza que la API no responda con un 200 OK imprevisto.
    """
    response = api_session.get(f"{base_url}/posts/%")
    assert response.status_code != 200, "El servidor no debería responder 200 OK ante un path inválido"


def test_get_inexistente_estructura(api_session, base_url):
    """
    Confirma que al solicitar un registro inexistente no se expongan
    atributos del modelo de negocio en la respuesta JSON.
    """
    response = api_session.get(f"{base_url}/posts/99999")
    data = response.json()
    assert isinstance(data, dict), "La respuesta debe ser un diccionario JSON"
    assert "id" not in data
    assert "title" not in data
    assert "body" not in data


def test_get_listado_estructura(api_session, base_url):
    """
    Comprueba que el endpoint de listado retorne una estructura de arreglo
    con la cantidad mínima esperada de elementos.
    """
    response = api_session.get(f"{base_url}/posts")
    data = response.json()
    assert isinstance(data, list), "La respuesta debe ser una lista de elementos"
    assert len(data) >= 100, f"Se esperaban al menos 100 elementos, se obtuvieron {len(data)}"


def test_get_validacion_campos_individual(api_session, base_url):
    """
    Valida que un registro existente posea sus campos clave válidos y no vacíos.
    """
    response = api_session.get(f"{base_url}/posts/1")
    data = response.json()

    assert data["id"] > 0, "El ID debe ser mayor a 0"
    assert isinstance(data["title"], str) and len(data["title"].strip()) > 0, "El título no debe estar vacío"
    assert isinstance(data["body"], str) and len(data["body"].strip()) > 0, "El cuerpo no debe estar vacío"


def test_get_validacion_campos_listado(api_session, base_url):
    """
    Recorre el conjunto de datos retornado asegurando que ningún elemento
    contenga atributos requeridos en None o vacíos.
    """
    response = api_session.get(f"{base_url}/posts")
    data = response.json()

    for idx, item in enumerate(data):
        assert item.get("userId") is not None, f"userId es nulo en el índice {idx}"
        assert item.get("id") is not None, f"id es nulo en el índice {idx}"
        assert bool(item.get("title")), f"title está vacío o es nulo en el índice {idx}"
        assert bool(item.get("body")), f"body está vacío o es nulo en el índice {idx}"


# ==========================================
# 2. MÉTODOS POST (PARAMETRIZADOS Y FIXTURES)
# ==========================================

@pytest.mark.parametrize("payload, codigos_esperados, descripcion", [
    ({}, [201, 400], "Body completamente vacío"),
    ({"title": "Solo título sin body ni userId"}, [201, 400, 422], "Payload con campos requeridos faltantes")
])
def test_post_escenarios_invalidos_parametrizados(api_session, base_url, payload, codigos_esperados, descripcion):
    """
    Prueba parametrizada para evaluar la creación de registros con payloads incompletos o vacíos.
    """
    response = api_session.post(f"{base_url}/posts", json=payload)
    assert response.status_code in codigos_esperados, (
        f"Falló en caso de '{descripcion}'. "
        f"Código devuelto: {response.status_code}, se esperaba uno de: {codigos_esperados}"
    )


def test_post_tipos_erroneos(api_session, base_url, payload_tipos_erroneos):
    """
    Usa la fixture 'payload_tipos_erroneos' definida en conftest.py
    para validar la sanitización cuando el tipo de dato es incorrecto.
    """
    response = api_session.post(f"{base_url}/posts", json=payload_tipos_erroneos)
    assert response.status_code in [201, 400, 422], f"Código inesperado: {response.status_code}"


def test_post_carga_extrema_overflow(api_session, base_url, payload_carga_extrema):
    """
    Usa la fixture 'payload_carga_extrema' definida en conftest.py
    para evaluar los límites de tamaño en los atributos del payload.
    """
    response = api_session.post(f"{base_url}/posts", json=payload_carga_extrema)
    assert response.status_code in [201, 400, 413], f"Código inesperado: {response.status_code}"


# ==========================================
# 3. MÉTODOS PUT / PATCH (PARAMETRIZADOS)
# ==========================================

@pytest.mark.parametrize("id_post, payload, codigos_esperados, descripcion", [
    (99999, {"userId": 1, "id": 99999, "title": "Prueba", "body": "Prueba"}, [200, 404, 500],
     "PUT a recurso inexistente"),
    (1, {}, [200, 400, 422, 500], "PUT con cuerpo vacío")
])
def test_put_escenarios_negativos_parametrizados(api_session, base_url, id_post, payload, codigos_esperados,
                                                 descripcion):
    """
    Evalúa fallas al actualizar recursos con payloads o identificadores inválidos.
    """
    response = api_session.put(f"{base_url}/posts/{id_post}", json=payload)
    assert response.status_code in codigos_esperados, (
        f"Falló escenario '{descripcion}'. Código devuelto: {response.status_code}"
    )


def test_patch_inyeccion_caracteres_especiales(api_session, base_url):
    """
    Valida la resistencia contra inyecciones XSS y SQL mediante PATCH.
    """
    payload = {
        "title": "<script>alert('xss')</script>",
        "body": "DROP TABLE posts; -- \"'//"
    }
    response = api_session.patch(f"{base_url}/posts/1", json=payload)
    assert response.status_code == 200, f"Se esperaba 200 OK, se obtuvo {response.status_code}"
    data = response.json()
    assert data["title"] == payload["title"], "La API debió procesar el texto sin romper el formato JSON"


# ==========================================
# 4. MÉTODOS DELETE (PARAMETRIZADOS)
# ==========================================

@pytest.mark.parametrize("id_recurso, codigos_esperados, descripcion", [
    ("99999", [200, 204, 404], "Eliminación de ID inexistente"),
    ("abc-invalid", [200, 400, 404, 500], "Eliminación con ID alfanumérico inválido")
])
def test_delete_escenarios_negativos_parametrizados(api_session, base_url, id_recurso, codigos_esperados, descripcion):
    """
    Prueba parametrizada para evaluar la eliminación de recursos inexistentes
    o con identificadores en formato no válido.
    """
    response = api_session.delete(f"{base_url}/posts/{id_recurso}")
    assert response.status_code in codigos_esperados, (
        f"Falló escenario '{descripcion}'. Código devuelto: {response.status_code}"
    )