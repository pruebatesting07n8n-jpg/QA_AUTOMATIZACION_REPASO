"""
==============================================================================
SUITE DE PRUEBAS DE INTEGRACIÓN API - COBERTURA HAPPY PATH Y PARAMETRIZADA
==============================================================================
Endpoint objetivo: JSONPlaceholder (https://jsonplaceholder.typicode.com)
Módulo objetivo: /posts y /posts/{id}

Estructura del archivo:
  1. TestGetListPosts  -> GET /posts (Colección)
  2. TestGetSinglePost -> GET /posts/{id} (Recurso Individual Parametrizado)
  3. TestPost          -> POST /posts (Creación Parametrizada / Data-Driven)
  4. TestPut           -> PUT /posts/1 (Actualización Total Parametrizada)
  5. TestPatch         -> PATCH /posts/1 (Actualización Parcial Parametrizada)
  6. TestDelete        -> DELETE /posts/1 (Eliminación)
==============================================================================
"""

import pytest
import requests


# ==============================================================================
# 1. PRUEBAS PARA GET /posts (COLECCIÓN COMPLETA)
# ==============================================================================

class TestGetListPosts:
    """
    Agrupa los casos de prueba para la consulta de la colección /posts.
    """

    def test_get_list_status_code_200(self, get_list_response):
        """[HTTP Status] Confirma que la respuesta devuelva HTTP 200 OK."""
        resp, _ = get_list_response
        assert resp.status_code == 200, f"Se esperaba HTTP 200 pero se recibió {resp.status_code}"

    def test_get_list_structure_is_list(self, get_list_response):
        """[Estructura Raíz] Evalúa que la respuesta sea un arreglo JSON (list)."""
        resp, body = get_list_response
        assert resp.status_code == 200, f"Se esperaba HTTP 200 pero se recibió {resp.status_code}"
        assert isinstance(body, list), f"Se esperaba una lista, pero se obtuvo {type(body).__name__}"

    def test_get_list_content_not_empty(self, get_list_response):
        """[Contenido] Garantiza que la colección devuelva elementos (longitud > 0)."""
        _, body = get_list_response
        assert len(body) > 0, "La lista de publicaciones devuelta está vacía"

    def test_get_list_content_type_header(self, get_list_response):
        """[Headers] Verifica que el Content-Type incluya application/json."""
        resp, _ = get_list_response
        assert "Content-Type" in resp.headers, "Falta la cabecera Content-Type"
        content_type = resp.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Content-Type no esperado: {content_type}"

    def test_get_list_response_time(self, get_list_response):
        """[SLA] Verifica que la latencia sea menor a 2000 ms."""
        resp, _ = get_list_response
        response_time_ms = resp.elapsed.total_seconds() * 1000
        assert response_time_ms < 2000, f"Latencia excesiva: {response_time_ms:.2f} ms"

    def test_get_list_item_schema(self, get_list_response):
        """[Contrato] Asegura que el primer objeto del listado contenga las llaves exactas."""
        _, body = get_list_response
        assert len(body) > 0, "No hay elementos para validar el esquema"
        first_item = body[0]
        expected_keys = {"id", "title", "body", "userId"}
        assert set(first_item.keys()) == expected_keys, "El esquema del elemento no coincide"


# ==============================================================================
# 2. PRUEBAS PARA GET /posts/{id} (RECURSO INDIVIDUAL PARAMETRIZADO)
# ==============================================================================

class TestGetSinglePost:
    """
    Agrupa los casos de prueba para la consulta de recursos individuales.
    Utiliza parametrización para verificar la consulta por distintos identificadores validos.
    """

    def test_get_single_status_code_200(self, get_response):
        """[HTTP Status] Confirma respuesta exitosa HTTP 200 OK para la fixture por defecto."""
        resp, _ = get_response
        assert resp.status_code == 200, f"Se esperaba HTTP 200 pero se recibió {resp.status_code}"

    @pytest.mark.parametrize("post_id", [1, 5, 10, 100])
    def test_get_single_post_by_multiple_ids(self, base_url, post_id):
        """
        [Data-Driven / GET] Consulta múltiples IDs existentes y valida
        que el recurso devuelto coincida exactamente con el ID solicitado.
        """
        url = f"{base_url}/posts/{post_id}"
        resp = requests.get(url)
        assert resp.status_code == 200, f"Falló consulta para post_id={post_id}"
        body = resp.json()
        assert body.get("id") == post_id, f"Se solicitó id={post_id} pero se recibió id={body.get('id')}"

    def test_get_single_data_types(self, get_response):
        """[Tipos de Datos] Confirma los tipos de los atributos (int y str)."""
        _, body = get_response
        assert isinstance(body.get("id"), int), "'id' no es entero"
        assert isinstance(body.get("userId"), int), "'userId' no es entero"
        assert isinstance(body.get("title"), str), "'title' no es string"
        assert isinstance(body.get("body"), str), "'body' no es string"

    def test_get_single_business_rules(self, get_response):
        """[Negocio] Valida que 'id' sea 1 y los campos de texto no estén vacíos."""
        _, body = get_response
        assert body.get("id") == 1, f"Se esperaba id=1, recibido: {body.get('id')}"
        title = body.get("title", "")
        body_text = body.get("body", "")
        assert len(title.strip()) > 0, "'title' no debe estar vacío"
        assert len(body_text.strip()) > 0, "'body' no debe estar vacío"


# ==============================================================================
# 3. PRUEBAS PARA POST /posts (CREACIÓN CON DATA-DRIVEN TESTING)
# ==============================================================================

class TestPost:
    """
    Agrupa las pruebas para la creación de publicaciones vía POST /posts.
    Incluye casos parametrizados con variaciones de datos y caracteres especiales.
    """

    def test_post_success_code(self, post_response):
        """[HTTP Status] Verifica el estado 201 Created para la petición base."""
        resp, _ = post_response
        assert resp.status_code == 201, f"Se esperaba HTTP 201 pero se recibió {resp.status_code}"

    @pytest.mark.parametrize("payload, desc", [
        ({"title": "Título Estándar", "body": "Contenido genérico", "userId": 1}, "Caso Estándar"),
        ({"title": "A" * 150, "body": "B" * 300, "userId": 1}, "Campos Largos / Límites"),
        ({"title": "Título con ÁEÍÓÚ ñ / @#$%", "body": "Texto con acentos y símbolos", "userId": 1}, "Caracteres Especiales"),
        ({"title": "12345", "body": "98765", "userId": 999}, "Valores Numéricos como String e ID Alto")
    ])
    def test_post_parametrized_payloads(self, base_url, payload, desc):
        """
        [Data-Driven / POST] Envía distintas variaciones de datos (caracteres especiales,
        textos largos, etc.) para validar la robustez de la creación de recursos.
        """
        url = f"{base_url}/posts"
        resp = requests.post(url, json=payload)

        assert resp.status_code == 201, f"Error en '{desc}': Se obtuvo {resp.status_code}"
        body = resp.json()
        assert body.get("title") == payload["title"], f"Error en '{desc}': El título no coincide"
        assert body.get("body") == payload["body"], f"Error en '{desc}': El body no coincide"
        assert body.get("userId") == payload["userId"], f"Error en '{desc}': El userId no coincide"
        assert isinstance(body.get("id"), int) and body.get("id") > 0, f"Error en '{desc}': ID inválido"

    def test_post_structure_is_object(self, post_response):
        """[Estructura Raíz] Evalúa que la respuesta sea un objeto JSON (dict)."""
        resp, body = post_response
        assert resp.status_code == 201, f"Se esperaba 201, se obtuvo {resp.status_code}"
        assert isinstance(body, dict), f"Se esperaba dict, pero se recibió {type(body).__name__}"

    def test_post_content_type_header(self, post_response):
        """[Headers] Confirma Content-Type: application/json."""
        resp, _ = post_response
        assert "Content-Type" in resp.headers, "Falta la cabecera Content-Type"
        content_type = resp.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Content-Type inesperado: {content_type}"

    def test_post_response_time(self, post_response):
        """[SLA] Valida que el tiempo de respuesta sea inferior a 2000 ms."""
        resp, _ = post_response
        response_time_ms = resp.elapsed.total_seconds() * 1000
        assert response_time_ms < 2000, f"Latencia excesiva: {response_time_ms:.2f} ms"

    def test_post_exact_contract_keys(self, post_response):
        """[Contrato] Verifica la coincidencia exacta de las llaves del objeto devuelto."""
        resp, body = post_response
        assert resp.status_code == 201, f"Se esperaba 201, se obtuvo {resp.status_code}"
        expected_keys = {"id", "title", "body", "userId"}
        actual_keys = set(body.keys())
        assert actual_keys == expected_keys, (
            f"Faltantes: {expected_keys - actual_keys} | Extras: {actual_keys - expected_keys}"
        )


# ==============================================================================
# 4. PRUEBAS PARA PUT /posts/1 (ACTUALIZACIÓN TOTAL PARAMETRIZADA)
# ==============================================================================

class TestPut:
    """
    Agrupa las pruebas para la actualización total de publicaciones vía PUT /posts/1.
    """

    def test_put_success_code(self, put_response):
        """[HTTP Status] Confirma el código de estado 200 OK."""
        resp, _, _ = put_response
        assert resp.status_code == 200, f"Se esperaba HTTP 200 pero se recibió {resp.status_code}"

    @pytest.mark.parametrize("payload, desc", [
        ({"id": 1, "title": "Nuevo Título PUT", "body": "Nuevo Cuerpo PUT", "userId": 1}, "Actualización Estándar"),
        ({"id": 1, "title": "Título con UTF-8: ¡Aparición!", "body": "Texto editado", "userId": 2}, "Cambio de userId y UTF-8")
    ])
    def test_put_parametrized_update(self, base_url, payload, desc):
        """
        [Data-Driven / PUT] Valida que la actualización total del recurso se realice
        correctamente para distintos datos de reemplazo.
        """
        url = f"{base_url}/posts/1"
        resp = requests.put(url, json=payload)

        assert resp.status_code == 200, f"Error en '{desc}': Se esperaba 200, recibido {resp.status_code}"
        body = resp.json()
        assert body.get("title") == payload["title"], f"Error en '{desc}': Título no actualizado"
        assert body.get("userId") == payload["userId"], f"Error en '{desc}': userId no actualizado"

    def test_put_content_type_header(self, put_response):
        """[Headers] Confirma la presencia de Content-Type: application/json."""
        resp, _, _ = put_response
        assert "Content-Type" in resp.headers, "Falta la cabecera Content-Type"
        content_type = resp.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Content-Type inesperado: {content_type}"

    def test_put_response_time(self, put_response):
        """[SLA] Mide la latencia asegurando respuesta < 2000 ms."""
        resp, _, _ = put_response
        response_time_ms = resp.elapsed.total_seconds() * 1000
        assert response_time_ms < 2000, f"Latencia excesiva: {response_time_ms:.2f} ms"


# ==============================================================================
# 5. PRUEBAS PARA PATCH /posts/1 (ACTUALIZACIÓN PARCIAL PARAMETRIZADA)
# ==============================================================================

class TestPatch:
    """
    Agrupa las pruebas para la actualización parcial vía PATCH /posts/1.
    """

    def test_patch_success_code(self, patch_response):
        """[HTTP Status] Confirma el código de estado 200 OK."""
        resp, _, _ = patch_response
        assert resp.status_code == 200, f"Se esperaba HTTP 200 pero se recibió {resp.status_code}"

    @pytest.mark.parametrize("partial_payload, field_key, expected_val", [
        ({"title": "Título Editado por PATCH"}, "title", "Título Editado por PATCH"),
        ({"body": "Solo actualizo el body en este PATCH"}, "body", "Solo actualizo el body en este PATCH")
    ])
    def test_patch_parametrized_single_field(self, base_url, partial_payload, field_key, expected_val):
        """
        [Data-Driven / PATCH] Actualiza campos individuales por separado y verifica
        que el campo modificado responda con el nuevo valor enviado.
        """
        url = f"{base_url}/posts/1"
        resp = requests.patch(url, json=partial_payload)

        assert resp.status_code == 200
        body = resp.json()
        assert body.get(field_key) == expected_val, f"El campo '{field_key}' no fue modificado correctamente"

    def test_patch_content_type_header(self, patch_response):
        """[Headers] Confirma la presencia de Content-Type: application/json."""
        resp, _, _ = patch_response
        assert "Content-Type" in resp.headers, "Falta el encabezado Content-Type"
        content_type = resp.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Content-Type inesperado: {content_type}"

    def test_patch_unmodified_data_integrity_and_types(self, patch_response):
        """[Persistencia y Tipos] Valida que id, userId y body mantengan su estado e integridad."""
        _, body, _ = patch_response
        assert isinstance(body.get("id"), int) and body.get("id") == 1, "id alterado o inválido"
        assert isinstance(body.get("userId"), int) and body.get("userId") == 1, "userId alterado"
        body_text = body.get("body", "")
        assert isinstance(body_text, str) and len(body_text.strip()) > 0, "body alterado o vacío"


# ==============================================================================
# 6. PRUEBAS PARA DELETE /posts/1 (ELIMINACIÓN DE RECURSO)
# ==============================================================================

class TestDelete:
    """
    Agrupa las pruebas para la eliminación de recursos vía DELETE /posts/1.
    """

    def test_delete_success_code(self, delete_response):
        """[HTTP Status] Confirma respuesta exitosa HTTP 200 OK."""
        resp, _ = delete_response
        assert resp.status_code == 200, f"Se esperaba HTTP 200 pero se obtuvo {resp.status_code}"

    def test_delete_content_type_header(self, delete_response):
        """[Headers] Confirma la presencia de Content-Type: application/json."""
        resp, _ = delete_response
        assert "Content-Type" in resp.headers, "Falta el encabezado Content-Type"
        content_type = resp.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Content-Type inesperado: {content_type}"

    def test_delete_response_time(self, delete_response):
        """[SLA] Valida latencia < 2000 ms."""
        resp, _ = delete_response
        response_time_ms = resp.elapsed.total_seconds() * 1000
        assert response_time_ms < 2000, f"Latencia excesiva: {response_time_ms:.2f} ms"

    def test_delete_contract_empty_object(self, delete_response):
        """[Contrato de Borrado] Audita que la respuesta sea un objeto diccionario limpio {}."""
        resp, body = delete_response
        assert resp.status_code == 200, f"Se esperaba 200, se obtuvo {resp.status_code}"
        assert isinstance(body, dict), f"Se esperaba dict, pero se obtuvo {type(body).__name__}"
        assert len(body) == 0, f"El objeto devuelto no está vacío, contiene {len(body)} llaves"

        business_keys = {"id", "title", "body", "userId"}
        found_keys = business_keys.intersection(set(body.keys()))
        assert len(found_keys) == 0, f"Se encontraron llaves de negocio tras el borrado: {found_keys}"

##JsonSchema
def test_validar_contrato_post(api_session, base_url, validar_esquema_post):
    """Verifica que el JSON devuelto por GET /posts/1 cumpla con el esquema definido."""
    response = api_session.get(f"{base_url}/posts/1")
    assert response.status_code == 200

    # Llama a la función de validación inyectada desde conftest.py
    validar_esquema_post(response.json())