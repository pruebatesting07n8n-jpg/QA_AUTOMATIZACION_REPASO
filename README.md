  Set-Content -Path README.md -Value '# QA Automation API Framework

![API Tests](https://github.com/pruebatesting07n8n-jpg/QA_AUTOMATIZACION_REPASO/actions/workflows/api_tests.yml/badge.svg)

Framework de automatización de pruebas de API empresarial desarrollado en Python utilizando **Pytest**, **Requests**, **JSON Schema**, y un pipeline automatizado de **CI/CD con GitHub Actions**.

---

## 🛠️ Tecnologías y Herramientas

* **Lenguaje:** Python 3.11+
* **Test Runner:** Pytest
* **HTTP Client:** Requests
* **Validación de Contratos:** JSonschema
* **Gestión de Entornos:** Python-dotenv
* **Reportes:** Pytest-html
* **CI/CD:** GitHub Actions (Ubuntu-latest)

---

## 📁 Estructura del Proyecto

```text
QA_AUTOMATIZACION_REPASO/
├── .github/
│   └── workflows/
│       └── api_tests.yml       # Configuración del Pipeline CI/CD
├── data/                       # Esquemas y datos de prueba
├── src/                        # Clases de soporte y módulos auxiliares
├── tests/                      # Suite de pruebas automatizadas (135 casos)
│   ├── conftest.py             # Fixtures y configuración centralizada
│   ├── test_01.py
│   ├── test_01_02_aaa.py
│   ├── test_02_02_parametrized.py
│   ├── test_04_02_conftest.py
│   ├── test_ahorro_casa.py
│   ├── test_api_request_CP_negativos.py
│   ├── test_api_requests_CP_HappyPath.py
│   └── test_suma_con_conftest.py
├── .env                        # Variables de entorno locales (no subidas a Git)
├── .gitignore                  # Exclusión de archivos sensibles/temporales
├── pytest.ini                  # Configuración global de Pytest
├── requirements.txt            # Dependencias del proyecto congeladas
└── README.md                   # Documentación del proyecto