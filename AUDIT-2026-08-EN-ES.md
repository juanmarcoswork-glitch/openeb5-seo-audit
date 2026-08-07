# Auditoría SEO — openeb5.com + /ES
**Fecha:** 7 de agosto de 2026
**Método:** crawl BFS propio de 215 URLs, verificación serial de códigos de estado, comparativa de stack de assets entre idiomas, Ahrefs Site Explorer
**Alcance:** 93 URLs en inglés + 122 URLs en español

---

## Resumen

| Métrica | Inglés | Español |
|---|---:|---:|
| URLs crawleadas | 93 | 122 |
| Respuestas 200 | 87 | 99 |
| Enlaces internos rotos (404) | 6 | 21 |
| URLs en sitemap | 67 | **0** |
| Páginas con `lang` correcto | 100% | **0%** |
| Páginas sin meta description | 12 | 33 |
| Páginas < 300 palabras | 8 | 10 |
| Imágenes sin `alt` | 0 | 0 |
| Bundles de plugins (home) | 10 | 24 |
| Scripts / hojas de estilo (home) | 18 / 28 | 29 / 64 |
| Caché HTTP | NitroPack | `no-store, no-cache` |

**Nota metodológica:** durante el crawl concurrente aparecieron 2 respuestas 503 en `/ES/proyectos-anteriores/` y un post del blog ES. Al reverificarlas en serie ambas devolvieron 200: eran limitación de tasa del propio crawler, no errores del sitio. **No se cuentan como incidencias.**

---

## 1. Enlaces rotos

### 1.1 Español — 21 URLs

Patrón sistemático: páginas en español enlazan a la ruta `/ES/` + **el slug en inglés**, que no existe.

| URL rota (404) | Debería apuntar a | Páginas que enlazan |
|---|---|---:|
| `/ES/contact-us/` | `/ES/contactanos/` | **22** |
| `/ES/spain/` | `/ES/espana/` | 6 |
| `/ES/brazil/` | `/ES/brasil/` | 6 |
| `/ES/south-korea/` | `/ES/corea-del-sur/` | 6 |
| `/ES/united-kingdom/` | `/ES/reino-unido/` | 6 |
| `/ES/eb-5-blog/` | `/ES/eb5-blog/` | 4 |
| `/ES/canada/` | no existe en ES ni EN | 4 |
| `/ES/france/` | no existe en ES ni EN | 4 |
| `/ES/turkey/` | no existe en ES ni EN | 4 |
| `/ES/venezuela/` | no existe en ES ni EN | 4 |
| `/ES/about-us/` | `/ES/nosotros/` | 2 |
| `/ES/the-team/` | `/ES/el-equipo/` | 2 |
| `/ES/countries/` | `/ES/paises/` | 2 |
| `/ES/current-projects/` | `/ES/proyectos-actuales/` | 2 |
| `/ES/collaborative-projects/` | `/ES/proyectos-colaborativos/` | 2 |
| `/ES/news/` | `/ES/noticias/` | 2 |
| `/ES/europe/` | `/ES/europa/` | 2 |
| `/ES/investors/` | `/ES/cuestionario-para-inversionistas/` | 2 |
| `/ES/the-complete-guide-to-eb-5-investment/` | `/ES/guia-integral-para-inversiones-eb5/` | 2 |
| `/ES/programa-eb-5/` | `/ES/eb-5/` | 1 |
| `/ES/ES/` | `/ES/` | 1 |

**El más costoso es `/ES/contact-us/`**: enlazado desde 22 páginas, casi todas entradas de blog. Es el enlace de conversión del sitio en español y está roto en toda la sección editorial.

### 1.2 Inglés — 6 URLs

| URL rota (404) | Páginas que enlazan | Nota |
|---|---:|---|
| `/terms/` | **90** | El footer sitewide. La página real es `/terms-of-service/` (200) |
| `/canada/` | 6 | Enlazada desde home, `/countries/`, `/eb-5/`, `/america/` |
| `/france/` | 6 | Enlazada desde home, `/countries/`, `/eb-5/`, `/europe/` |
| `/turkey/` | 6 | Enlazada desde home, `/countries/`, `/eb-5/`, `/asia/` |
| `/venezuela/` | 6 | Enlazada desde home, `/countries/`, `/eb-5/`, `/america/` |
| `/blog/page/2/` | 1 | Paginación de `/blog/`. `/eb-5-blog/page/2/` sí funciona |

### 1.3 Sensibilidad a mayúsculas

- `/ES/` → **200**
- `/ES` → 301 correcto a `/ES/`
- `/es/` → **404**

Falta un 301 de `/es/*` a `/ES/*`.

---

## 2. Indexación

### 2.1 El sitio en español no está en el sitemap

`sitemap_index.xml` declara 4 sub-sitemaps con 67 URLs. **Ninguna contiene `/ES/`.**

| Sub-sitemap | URLs | Última modificación |
|---|---:|---|
| `post-sitemap.xml` | 25 | 2026-07-31 |
| `page-sitemap.xml` | 38 | 2026-07-14 |
| `category-sitemap.xml` | 1 | 2026-07-31 |
| `post_tag-sitemap.xml` | 3 | 2026-06-14 |

`/es-sitemap.xml` devuelve 404. No existe sitemap alternativo para español.

### 2.2 URLs que redirigen dentro del sitemap

- `/brownsville-parkside/` → 301 → `/current-projects/brownsville-parkside/`
- `/midtown-pharr/` → 301 → `/current-projects/midtown-pharr/`

### 2.3 robots.txt — regresión

El archivo en vivo es el bloque por defecto de Yoast:

```
# START YOAST BLOCK
User-agent: *
Disallow:
Sitemap: https://openeb5.com/sitemap_index.xml
# END YOAST BLOCK
```

**El bloque de 8 AI crawlers añadido en junio de 2026 ya no está.** Probable reescritura por actualización de Yoast o del tema. Debe restituirse vía filtro `robots_txt` del tema para que persista.

---

## 3. Señales de idioma

### 3.1 Atributo `lang` incorrecto en el 100% del sitio español

Las **122 páginas** bajo `/ES/` declaran `<html lang="en-US">`, sin una sola excepción. Incluye las páginas que rankean en México, Chile, Argentina y España.

### 3.2 hreflang invertido

**Home en inglés (correcto):**
```
en-US     → https://openeb5.com/
es        → https://openeb5.com/ES/
x-default → https://openeb5.com/
```

**Home en español (roto):**
```
en-US     → https://openeb5.com/ES/
es        → https://openeb5.com/ES/ES/
x-default → https://openeb5.com/ES/
```

El generador **antepone `/ES/` a una URL que ya lo tiene** en lugar de calcular la pareja de idioma real. La versión española se declara a sí misma como inglesa, y señala una URL inventada como su versión española.

Además, **68 de 180 páginas indexables no emiten hreflang en absoluto**, incluidas todas las entradas del blog en ambos idiomas.

### 3.3 Espacio fantasma `/ES/ES/`

Consecuencia directa: existe un árbol completo de 38 URLs duplicadas bajo `/ES/ES/`. La mayoría redirige con 301, pero `/ES/ES/` a secas **devuelve 404 y está enlazada desde la home en español**.

---

## 4. Metadatos

### 4.1 Meta descriptions faltantes

**Español (33):** las 13 entradas del blog; 16 páginas de país (argentina, australia, brasil, chile, china, colombia, corea-del-sur, espana, india, israel, mexico, pakistan, peru, reino-unido, taiwan, vietnam); `/ES/noticias/`, `/ES/lp-guia/`, `/ES/privacy-policy/`, `/ES/terms-of-service/`.

**Inglés (12):** `/blog/`, `/category/blog/`, `/terms-of-service/`, `/brownsville-parkside/`, `/current-projects/brownsville-parkside/` y las 6 páginas de `/tag/`.

### 4.2 Meta descriptions fuera de rango

| URL | Caracteres |
|---|---:|
| `/ES/midtown-brownsville-ii/` | 341 |
| `/ES/advisory-board/` | 178 |
| `/blog/strategic-investment-with-open-eb5/` | 166 |

### 4.3 Títulos

**Plantilla del blog ES demasiado larga.** El sufijo ` - Open EB5 | Green Card` gasta 24 caracteres. **12 de 13 posts superan los 60 caracteres.** Los peores:

| Caracteres | Título |
|---:|---|
| 113 | Guía de la Visa de Inversionista EB-5: Requisitos, Costos y el Camino hacia la Green Card - Open EB5 \| Green Card |
| 111 | ¿Qué pasa después de navegar el programa de visa EB-5 por EB-5? Etapas y próximos pasos - Open EB5 \| Green Card |
| 108 | Inversión Estratégica con Open EB5: Obtén la Residencia Permanente en Estados Unidos - Open EB5 \| Green Card |
| 107 | Texas, el Lugar Ideal para Invertir y Obtener tu residencia permanente con Open EB5 - Open EB5 \| Green Card |

El de 111 caracteres tiene además una **redacción rota**: "navegar el programa de visa EB-5 por EB-5" parece un buscar-y-reemplazar mal aplicado. Debería decir "obtener la Green Card por EB-5".

**Títulos demasiado cortos y sin keyword (4 páginas de país ES):** `/ES/chile/`, `/ES/china/`, `/ES/india/`, `/ES/peru/`, todas del tipo "Chile - Open EB5 | Green Card" (28-29 caracteres). Contrasta con el resto de páginas de país ES, que sí usan un patrón trabajado ("Programa EB5 América: Evalúe sus Opciones en EE. UU.").

### 4.4 Títulos duplicados

| Título | URLs |
|---|---|
| Blog Programa EB5: Artículos y Guías Oficiales en EE. UU. | 4 (`/ES/eb5-blog/` + variantes de paginación y `/ES/ES/`) |
| EB5 Blog: Expert Insights for Foreign Investors | 3 (`/eb-5-blog/` + paginación) |
| Proyecto Midtown Pharr: Conozca Nuestro Desarrollo EB5 | 3 |
| Blog Archives - openeb5 | 2 (`/blog/` y `/category/blog/`) |
| Contact Open EB5 \| Schedule a Free Consultation Today | 2 (`/contact-us/` y `/lp-contact-us/`) |
| Midtown Pharr EB5 Project \| Texas Real Estate | 2 |
| Brownsville Parkside - openeb5 | 2 |

---

## 5. Estructura de contenido

### 5.1 H1 duplicados y sin traducir (4 páginas ES)

| URL | H1 #1 | H1 #2 |
|---|---|---|
| `/ES/corea-del-sur/` | Corea del Sur | "Expand Your Horizons with EB5 Investment" (inglés) |
| `/ES/reino-unido/` | Reino Unido | "Build Your American Legacy & Expand…" (inglés) |
| `/ES/brasil/` | Brasil | "Investimento Estratégico nos EUA" (portugués) |
| `/ES/espana/` | España | "Construye tu legado en los Estados Unido" (truncado) |

### 5.2 Contenido corto

**Español (10):** `/ES/noticias/` 69 pal., `/ES/corea-del-sur/` 93, `/ES/reino-unido/` 122, `/ES/lp-guia/` 125, `/ES/espana/` 133, `/ES/brasil/` 135, `/ES/oceania/` 166, `/ES/europa/` 177, `/ES/proyectos-colaborativos/` 191, `/ES/america/` 199.

**Inglés (8):** `/brownsville-parkside/` 73 pal., `/collaborative-projects/` 163, `/oceania/` 175, `/europe/` 179, `/america/` 202, `/asia/` 202, `/countries/` 274, `/current-projects/` 286.

`/ES/espana/` merece prioridad: España es un mercado donde el sitio ya rankea (#7 para "eb5") y la página tiene 133 palabras.

### 5.3 Canonicals

Solo 3 discrepancias, todas de paginación y una de arquitectura:

- `/blog/` canonicaliza a `/category/blog/`
- `/eb-5-blog/page/2/` canonicaliza a `/eb-5-blog/`
- `/ES/eb5-blog/page/2/` canonicaliza a `/ES/eb5-blog/`

Las de paginación son aceptables; la de `/blog/` refleja el problema de tres archivos coexistiendo.

---

## 6. Rendimiento

### 6.1 Medición en vivo

| URL | TTFB | Scripts | Hojas CSS | Caché |
|---|---:|---:|---:|---|
| `/` | 2,11 s | 18 | 28 | NitroPack `MISS` |
| `/eb-5/` | 2,11 s | 18 | 28 | NitroPack |
| `/current-projects/` | 1,39 s | 18 | 28 | NitroPack |
| `/ES/` | 1,94 s | 29 | 64 | `no-store, no-cache` |
| `/ES/eb-5/` | 1,64 s | 27 | 58 | `no-store, no-cache` |
| `/ES/proyectos-actuales/` | 1,64 s | 27 | 57 | `no-store, no-cache` |

TTFB de 1,4 a 2,1 s en ambos idiomas (objetivo razonable: menos de 0,8 s).

### 6.2 Las optimizaciones no llegaron al español

Bundles de plugins cargados:

**Inglés (10):** contact-form-7, country-phone-field-contact-form-7, elementor, elementskit, elementskit-lite, google-site-kit, mailchimp-for-wp, openeb5-form-to-pdf, whatsapp-for-wordpress.

**Español (24):** los anteriores **más** booked, case-theme-core, case-theme-user, elementor-pro, emage-hover-effects-for-elementor, google-analytics-for-wordpress, instagram-feed, massive-cryptocurrency-widgets, meks-simple-flickr-widget, newsletter, **revslider**, **woocommerce**, yith-woocommerce-quick-view, yith-woocommerce-wishlist.

Los dequeues de las Fases 1-4 se aplicaron con una condición que excluye las rutas `/ES/`. El sitio que rankea se sirve en la peor configuración de la propiedad.

**No se pudo obtener PageSpeed Insights**: la cuota diaria de la API sin clave estaba agotada al momento de la auditoría. Las métricas de laboratorio (LCP, CLS, TBT) deberán tomarse con clave de API o desde la interfaz web.

---

## 7. Schema y GEO

### 7.1 Schema — en buen estado

17 tipos distintos detectados en el HTML en vivo.

**Home EN:** `FinancialService`, `LocalBusiness`, `Organization`, `Person` ×2, `WebSite`, `WebPage`, `GeoCoordinates`, `OpeningHoursSpecification`, `PostalAddress` ×2, `VideoObject`, `ImageObject` ×2, `SearchAction`, `EntryPoint`, `ReadAction`, `PropertyValue`, y 21 nodos `Country`.

**Posts EN:** se suma `Article` + `BreadcrumbList` + `ListItem` ×3.

**Home ES:** idéntica **salvo que falta el nodo `Organization`**.

### 7.2 llms.txt

Responde 200 con contenido correcto. Pendientes:

- Fechado `2026-06-14`
- **No incluye ninguna URL en español**
- No menciona la aprobación I-956F de Midtown Pharr

### 7.3 Imágenes

**0 imágenes sin atributo `alt`** en las 215 páginas, en ambos idiomas. Punto cerrado.

---

## 8. Autoridad orgánica

Ahrefs Site Explorer, 7 de agosto de 2026, modo subdominios:

- **4 keywords orgánicas**
- **1 visita orgánica estimada al mes**
- 1 keyword en el top 3
- 0 keywords de pago

| Keyword | País | Posición | Volumen | URL |
|---|---|---:|---:|---|
| eb-5 | Argentina | 1 | 10 | `/ES/` |
| eb5 | Argentina | 6 | 30 | `/ES/` |
| eb5 | España | 7 | 40 | `/ES/` |
| eb5 | Chile | 8 | 150 | `/ES/` |
| eb5 | México | 9 | 100 | `/ES/` |
| what is green card | Singapur | 8 | 20 | `/blog/what-is-the-green-card…` |
| que es la green card | EE. UU. | 27 | 500 | `/ES/blog/que-es-la-green-card…` |

**Cinco de las siete posiciones registradas apuntan a `/ES/`.** El sitio en español es el activo orgánico del proyecto.

---

## 9. Reproducir esta auditoría

```bash
# 1. Descargar sitemaps y extraer URLs
for s in page post category post_tag; do
  curl -s "https://openeb5.com/${s}-sitemap.xml" -A "Mozilla/5.0" > sm-$s.xml
done
grep -ho '<loc>[^<]*</loc>' sm-*.xml | sed 's/<[^>]*>//g' | sort -u > all-urls.txt

# 2. Crawl BFS de ambos idiomas (script en data/crawl.py)
python crawl.py          # genera crawl.json

# 3. Análisis (script en data/analyze.py)
PYTHONIOENCODING=utf-8 python analyze.py > analysis.txt
```

Los scripts `crawl.py` y `analyze.py` están en `data/`. El crawler siembra desde `all-urls.txt` más las dos homes, sigue enlaces internos, descarta assets y parámetros de consulta, y tope en 400 páginas.

**Advertencia:** el crawler usa 12 hilos. Con esa concurrencia el servidor devuelve 503 esporádicos. Toda incidencia debe reverificarse en serie antes de reportarla.
