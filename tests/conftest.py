import pytest
import requests

@pytest.fixture
def setup_datos_suma():
    return [
        {"test_name": "numeros positivos","a":3, "b":4, "re":7},
        {"test_name": "numeros negativos", "a": -1, "b": -1, "re": -2}
    ]

@pytest.fixture
def hola_soy_conftest():
    print("Hola soy in fixture heredado desde  conftest")

@pytest.fixture
def driver():
    driver = "Chrome"
    print(f"Creando driver automatizado: {driver}")
    yield driver
    #driver.quit()
    print(f"Terminando driver automatizado: {driver}")
# ==============================================================================
# NUEVO: FIXTURE AGREGADO PARA SOLUCIONAR EL ERROR DE CONEXIÓN INDIRECTA
# ==============================================================================
@pytest.fixture
def login_data(request):
    """
    Recibe dinámicamente los parámetros desde el decorador
    @pytest.mark.parametrize(..., indirect=True) en el archivo de prueba.
    """
    # request.param contendrá la tupla de datos enviada desde el test
    return request.param




# ==============================================================================
# CONFIGURACIÓN GENERAL Y VARIABLES GLOBALES
# ==============================================================================

@pytest.fixture(scope="session")
def base_url():
    """
    [URL Base de la API]
    Define la dirección raíz centralizada para todas las peticiones HTTP.
    El scope='session' asegura que esta URL se instancie una sola vez por ejecución.
    """
    return "https://jsonplaceholder.typicode.com"


# ==============================================================================
# FIXTURES PARA PETICIONES GET (CONSULTA DE RECURSOS)
# ==============================================================================

@pytest.fixture
def get_response(base_url):
    """
    [Petición GET - Recurso Individual]
    Consulta la información de una publicación específica (/posts/1).
    Maneja excepciones de forma segura al deserializar la respuesta a un dict {}.

    Returns:
        tuple: (Response de requests, dict con el JSON deserializado)
    """
    url = f"{base_url}/posts/1"
    resp = requests.get(url)

    try:
        body = resp.json()
    except Exception:
        body = {}

    return resp, body


@pytest.fixture
def get_list_response(base_url):
    """
    [Petición GET - Colección / Lista]
    Consulta el listado completo de publicaciones (/posts).
    Maneja excepciones de forma segura al deserializar la respuesta a una list [].

    Returns:
        tuple: (Response de requests, list con el JSON deserializado)
    """
    url = f"{base_url}/posts"
    resp = requests.get(url)

    try:
        body = resp.json()
    except Exception:
        body = []

    return resp, body


# ==============================================================================
# FIXTURES PARA PETICIONES POST Y PUT (CREACIÓN Y ACTUALIZACIÓN)
# ==============================================================================

@pytest.fixture
def post_response(base_url):
    """
    [Petición POST - Creación de Recurso]
    Envía un payload de prueba al endpoint /posts usando json=data para:
      1. Convertir el diccionario de Python a una cadena JSON válida.
      2. Asignar automáticamente el encabezado Content-Type: application/json.

    Returns:
        tuple: (Response de requests, dict con la respuesta de la API)
    """
    url = f"{base_url}/posts"
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }

    resp = requests.post(url, json=payload)
    return resp, resp.json()


@pytest.fixture
def put_response(base_url):
    """
    [Petición PUT - Actualización Total]
    Envía una solicitud de actualización sobre /posts/1 con los datos modificados.
    Retorna el payload enviado para permitir aserciones dinámicas en los tests (Echo Test).

    Returns:
        tuple: (Response de requests, dict con la respuesta, dict con los datos enviados)
    """
    url = f"{base_url}/posts/1"
    payload = {
        "id": 1,
        "title": "foo_updated",
        "body": "bar_updated",
        "userId": 1
    }

    resp = requests.put(url, json=payload)
    return resp, resp.json(), payload


@pytest.fixture
def patch_response(base_url):
    """
    [Petición PATCH - Actualización Parcial]
    Envia una solicitud PATCH sobre /posts/1 modificando únicamente el título.
    Retorna la respuesta HTTP, el JSON deserializado y el payload parcial enviado
    para permitir comparaciones dinámicas en los tests (Echo Test Parcial).

    Returns:
        tuple: (Response de requests, dict con la respuesta, dict con los datos enviados)
    """
    url = f"{base_url}/posts/1"

    # Enviamos solo la propiedad que deseamos actualizar
    payload = {
        "title": "title_patched"
    }

    resp = requests.patch(url, json=payload)
    return resp, resp.json(), payload

## delete
@pytest.fixture
def delete_response(base_url):
    """
    [Petición DELETE - Eliminación de Recurso]
    Envía una solicitud DELETE sobre /posts/1 para confirmar la destrucción del recurso.
    Maneja la deserialización del cuerpo vacío de forma segura.

    Returns:
        tuple: (Response de requests, dict con la respuesta deserializada)
    """
    url = f"{base_url}/posts/1"
    resp = requests.delete(url)

    try:
        body = resp.json()
    except Exception:
        body = {}

    return resp, body

##Casos negativos

import pytest
import requests


# ==========================================
# 1. CONFIGURACIÓN Y CLIENTE HTTP
# ==========================================

@pytest.fixture(scope="session")
def base_url():
    """
    Proporciona la URL base para el entorno de pruebas.
    Permite cambiar fácilmente el entorno (dev, qa, prod) desde un solo lugar.
    """
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_session():
    """
    Crea una sesión HTTP única de `requests` compartida durante toda la ejecución.
    - Reutiliza conexiones TCP (mejora la velocidad de ejecución).
    - Configura encabezados predeterminados (Content-Type, Accept) para todas las peticiones.
    - Cierra la sesión automáticamente al finalizar las pruebas.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json"
    })

    yield session

    # Limpieza: Cierra la sesión al terminar
    session.close()


# ==========================================
# 2. FIXTURES DE DATOS / PAYLOADS DE PRUEBA
# ==========================================

@pytest.fixture
def payload_tipos_erroneos():
    """
    Suministra un objeto JSON con tipos de datos alterados / no válidos
    para probar reglas de validación y sanitización en POST/PUT.
    """
    return {
        "userId": "texto_invalido",  # Se espera entero
        "title": True,  # Se espera string
        "body": 12345  # Se espera string
    }


@pytest.fixture
def payload_carga_extrema():
    """
    Suministra un objeto JSON con cadenas de texto extremadamente largas
    para verificar el comportamiento ante desbordamientos o límites de payload.
    """
    return {
        "userId": 1,
        "title": "A" * 1000,
        "body": "B" * 20000
    }

# ==========================================
# PERSONALIZACIÓN DEL REPORTE HTML
# ==========================================
# ==========================================
# PERSONALIZACIÓN DEL REPORTE HTML
# ==========================================

def pytest_html_report_title(report):
    report.title = "Reporte General de Automatización - APIs (Positivos y Negativos)"


def pytest_configure(config):
    # Asigna metadatos solo si el plugin pytest-metadata está disponible
    if hasattr(config, "_metadata"):
        config._metadata["Codigo Facilito"] = "Pruebas de API - JSONPlaceholder"
        config._metadata["Módulos3"] = "Happy Path (Positivos) y Escenarios Negativos"
        config._metadata["Prueba"] = "QA / Testing"

## jsonschema
from jsonschema import validate

# Definición del contrato / esquema JSON para un Post
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "number"},
        "id": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["userId", "id", "title", "body"]
}

@pytest.fixture
def validar_esquema_post():
    """Fixture que valida la estructura JSON de una respuesta según el contrato POST_SCHEMA."""
    def _validar(data):
        validate(instance=data, schema=POST_SCHEMA)
    return _validar

## env
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")