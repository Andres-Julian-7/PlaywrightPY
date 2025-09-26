# PlaywrightPY

Automatización de prueba end-to-end con Playwright en Python para validar la búsqueda de productos en coppel.com.

## Requisitos

- Python 3.12.8
- virtualenv
- Paquetes instalados en el entorno: pip, pytest, requests
- Playwright (se instala más abajo)

## Configuración del entorno

1) Crear y activar entorno virtual
- Linux/macOS:
  - python3 -m venv .venv
  - source .venv/bin/activate
- Windows (PowerShell):
  - py -3 -m venv .venv
  - .\.venv\Scripts\Activate.ps1

2) Instalar dependencias
- pip install pytest playwright

3) Instalar navegadores de Playwright
- python -m playwright install
- Opcional (soporte para ffmpeg, etc.):
  - python -m playwright install-deps  (Linux)

## Estructura

- test_coppel.py: Prueba con Pytest + Playwright que valida una búsqueda y presencia de resultados con “300”.
- playwright.yml: Configuración opcional de Playwright (si se usa CI/acciones).

## Ejecución de pruebas

- Ejecutar todas las pruebas:
  - pytest -q
- Ejecutar una prueba específica:
  - pytest -q test_coppel.py::test_busqueda_coppel_moto_vento_300
- Con trazas/diagnóstico de Playwright:
  - pytest -q --tracing=on
- Con headed (navegador visible):
  - pytest -q --headed
- Con un navegador específico:
  - pytest -q --browser chromium
  - pytest -q --browser firefox
  - pytest -q --browser webkit

Sugerencia: si tu red tiene bloqueos o problemas intermitentes, usa reintentos de Pytest:
- pytest -q --maxfail=1 --reruns 2 --reruns-delay 2

(Para usar --reruns instala pytest-rerunfailures: pip install pytest-rerunfailures)

## Variables y entorno

- Si necesitas proxies o configuración regional, puedes exportar variables de entorno antes de ejecutar Pytest, por ejemplo:
  - HTTP_PROXY, HTTPS_PROXY
  - PLAYWRIGHT_BROWSERS_PATH

## Buenas prácticas

- Mantén los selectores robustos (data-testid cuando sea posible).
- Evita sleeps fijos; usa esperas explícitas de Playwright (wait_for, expect).
- Aísla estado entre pruebas usando contextos/nuevas páginas por test.
- Usa fixtures de Pytest/Playwright para crear contextos y páginas de forma consistente.

## Solución de problemas

- Si falla la instalación de navegadores:
  - python -m playwright install --with-deps
- Si la página muestra modales que bloquean:
  - Revisa y actualiza los selectores de cierre en la prueba.
- Si cambian las rutas/URLs del sitio:
  - Ajusta la validación del patrón de URL en la prueba.

## CI/CD (opcional)

- En entornos CI, recuerda:
  - Instalar dependencias de sistema necesarias (Linux): python -m playwright install-deps
  - Instalar navegadores: python -m playwright install
  - Ejecutar pytest con trazas: pytest --tracing=retain-on-failure
  - Publicar artefactos de traces/videos si los habilitas.
