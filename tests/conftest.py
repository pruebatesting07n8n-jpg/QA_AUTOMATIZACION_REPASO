import pytest

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
