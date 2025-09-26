import re
from playwright.sync_api import Page, expect

def test_busqueda_coppel_moto_vento_300(page: Page, context):
    # Configurar UA y desactivar http2 creando un nuevo contexto (si tu fixture lo permite, usa context directamente)
    # Nota: si ya usas fixtures de Playwright, puedes mover estas opciones a la creación del contexto.
    context.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"})
    # Cookie de consentimiento aproximada (dominio base). Ajuste defensivo: expira en 1 año.
    context.add_cookies([{
        "name": "cookie_consent",
        "value": "accepted",
        "domain": ".coppel.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])

    # Intento con reintentos por posibles errores transitorios HTTP2
    last_error = None
    for _ in range(2):
        try:
            page.goto("https://www.coppel.com/", wait_until="load", timeout=60000)
            break
        except Exception as e:
            last_error = e
            page.wait_for_timeout(1500)
    else:
        raise last_error

    # Cerrar banners/modales comunes
    for sel in [
        "button:has-text('Aceptar')",
        "button:has-text('Entendido')",
        "button:has-text('Continuar')",
        "button[aria-label='Cerrar']",
        "[data-testid='close-button']",
        "div[role='dialog'] button:has-text('Aceptar')",
    ]:
        try:
            page.locator(sel).first.click(timeout=1200)
        except Exception:
            pass

    # Buscar
    term = "moto vento motor 300"
    search_box = page.locator("input[type='search'], input[placeholder*='Buscar' i]").first
    search_box.wait_for(state="visible", timeout=15000)
    search_box.click()
    search_box.fill(term)
    search_box.press("Enter")

    # Esperar resultados
    expect(page).to_have_url(re.compile(r"coppel\.com/.+(search|result|buscar|s\?)"), timeout=60000)

    items = page.locator("article:has(a[href*='/p/']), [data-testid*='product'], [class*='product-card']")
    # A veces tarda en hidratar; espera a que haya al menos un elemento con texto
    expect(items).to_have_count(lambda c: c >= 1, timeout=60000)

    title_locators = items.locator("a[title], h2, h3, [data-testid*='title'], [class*='title'], [class*='name']")
    title_locators.first.wait_for(state="visible", timeout=20000)

    texts = [t.strip() for t in title_locators.all_text_contents() if t and t.strip()]
    assert texts, "No se encontraron títulos de productos en los resultados."

    assert any("300" in t for t in texts), f"Ningún producto contiene '300'. Muestras: {texts[:5]}"