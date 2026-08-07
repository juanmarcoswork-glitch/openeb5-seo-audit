# Scope of Work — Open EB5 SEO
**Versión:** 1.0
**Fecha:** 7 de agosto de 2026
**Alcance:** openeb5.com (inglés) + openeb5.com/ES/ (español)
**Preparado por:** Juan Marcos, SEO Specialist
**Panel en vivo:** https://juanmarcoswork-glitch.github.io/openeb5/seo-audit/

---

## 1. Punto de partida

Re-auditoría completa ejecutada el 7 de agosto de 2026 sobre un crawl propio de **215 URLs reales** (93 en inglés, 122 en español), verificando en vivo códigos de estado, títulos, meta descriptions, H1, canonicals, hreflang, atributo `lang`, directivas robots, conteo de palabras, atributos `alt`, cabeceras HTTP y stack de assets.

La auditoría de mayo de 2026 cubrió únicamente la versión en inglés. **Esta es la primera vez que se audita `/ES/` con el mismo rigor.**

### El hallazgo que define la prioridad

Según Ahrefs (7 Ago 2026), el dominio tiene **4 keywords orgánicas** y **1 visita orgánica estimada al mes**. De las 7 posiciones registradas, **5 apuntan a `/ES/`**:

| Keyword | País | Posición | Volumen | URL |
|---|---|---:|---:|---|
| eb5 | Argentina | 6 | 30 | `/ES/` |
| eb5 | España | 7 | 40 | `/ES/` |
| eb5 | Chile | 8 | 150 | `/ES/` |
| eb5 | México | 9 | 100 | `/ES/` |
| eb-5 | Argentina | 1 | 10 | `/ES/` |
| que es la green card | EE. UU. | 27 | 500 | `/ES/blog/que-es-la-green-card…` |
| what is green card | Singapur | 8 | 20 | `/blog/what-is-the-green-card…` |

**El activo orgánico real de Open EB5 es el sitio en español**, y es exactamente el que quedó fuera de todas las optimizaciones de las Fases 1 a 4.

### Estado técnico resumido

| Métrica | Inglés | Español |
|---|---:|---:|
| URLs crawleadas | 93 | 122 |
| Enlaces internos rotos (404) | 6 | 21 |
| URLs declaradas en sitemap | 67 | **0** |
| Páginas con `lang` correcto | 100% | **0%** |
| Bundles de plugins cargados | 10 | **24** |
| Hojas de estilo (home) | 28 | **64** |
| Caché HTTP | NitroPack | **`no-store`** |
| Imágenes sin `alt` | 0 | 0 |

**Score de la propiedad completa: 58/100.** (El 62/100 de junio se midió solo sobre inglés; el cambio refleja ampliación del alcance de medición, no un retroceso, salvo una regresión real en `robots.txt`.)

---

## 2. Fase 1 — Reparación de fundamentos

**Duración:** 4 semanas (11 Ago – 5 Sep 2026)
**Esfuerzo:** 43 horas
**Estructura:** 1 tarea técnica + 2 tareas on-page por semana

### Semana 1 (11–15 Ago) — Que Google vea el español

| Tipo | Tarea | Horas |
|---|---|---:|
| **Técnica** | **T1 · Sitemap ES + atributo `lang`.** Incluir las ~40 URLs de `/ES/` en el sitemap de Yoast (o generar `/ES/sitemap.xml` y referenciarlo desde el índice). Corregir el `<html lang>` para que las rutas `/ES/` emitan `es` en lugar de `en-US`. Enviar sitemap en Search Console. | 4 h |
| On-Page | **O1 · 13 meta descriptions del blog ES.** Ninguna de las 13 entradas en español tiene meta description. Redactar 140-155 caracteres con keyword y CTA. Empezar por `que-es-la-green-card…` (ya rankea #27 en EE. UU., 500 búsquedas/mes). | 3 h |
| On-Page | **O2 · Plantilla de títulos del blog ES.** Cambiar el sufijo ` - Open EB5 \| Green Card` (24 car.) por ` \| Open EB5`. 12 de 13 posts superan hoy los 60 caracteres. Reescribir los 4 más largos (hasta 113 car.) y corregir el título roto "¿Qué pasa después de navegar el programa de visa EB-5 por EB-5?". | 2 h |

**Verificación:** sitemap lista URLs ES; `curl` sobre 5 páginas ES devuelve `lang="es"`.

### Semana 2 (18–22 Ago) — Reparar lo roto

| Tipo | Tarea | Horas |
|---|---|---:|
| **Técnica** | **T2 · 27 enlaces rotos + reglas 301.** ES (21): corregir enlaces a `/ES/` + slug inglés; prioridad `/ES/contact-us/`, roto en 22 páginas. EN (6): `/terms/` en el footer (90 páginas) → `/terms-of-service/`; `/blog/page/2/`; `/canada/`, `/france/`, `/turkey/`, `/venezuela/`. Extra: 301 de `/es/` minúsculas → `/ES/`; sacar del sitemap las 2 URLs que redirigen. | 5 h |
| On-Page | **O3 · Títulos y metas de países ES.** `/ES/chile/`, `/ES/china/`, `/ES/india/`, `/ES/peru/` tienen títulos de 28-29 caracteres sin keyword ("Chile - Open EB5 \| Green Card"). Reescribir con el patrón que ya funciona. Añadir meta description a las 16 páginas de país ES. | 2 h |
| On-Page | **O4 · H1 duplicados y sin traducir.** `/ES/brasil/`, `/ES/corea-del-sur/`, `/ES/espana/` y `/ES/reino-unido/` tienen 2 H1, con el segundo en inglés, en portugués o truncado. Dejar un H1 y traducir. | 2 h |

**Verificación:** re-crawl completo con 0 respuestas 404 en las 215 URLs.

### Semana 3 (25–29 Ago) — Señales limpias y contenido

| Tipo | Tarea | Horas |
|---|---|---:|
| **Técnica** | **T3 · hreflang + espacio `/ES/ES/`.** Reescribir `inc/hreflang.php` para calcular la pareja de idioma real en lugar de anteponer `/ES/` a la URL actual. Requiere mapa explícito de equivalencias de slugs. Eliminar el enlace a `/ES/ES/` de la home ES y añadir 301 de `/ES/ES/*` → `/ES/*` (38 URLs fantasma). | 5 h |
| On-Page | **O5 · Ampliar 5 páginas ES cortas** a mínimo 400 palabras: `/ES/espana/` (133 pal., prioridad: España rankea #7), `/ES/corea-del-sur/` (93), `/ES/reino-unido/` (122), `/ES/brasil/` (135), `/ES/noticias/` (69). Cubrir requisitos locales, plazos, origen de fondos y un dato de mercado. | 6 h |
| On-Page | **O6 · Meta descriptions fuera de rango + faltantes EN.** Recortar `/ES/midtown-brownsville-ii/` (341 car.) y `/ES/advisory-board/` (178). Completar las 12 páginas EN sin descripción y recortar `/blog/strategic-investment-with-open-eb5/` (166 car.). | 3 h |

**Verificación:** 0 URLs bajo `/ES/ES/`; hreflang recíproco correcto en 10 pares de páginas.

### Semana 4 (1–5 Sep) — Velocidad y consolidación

| Tipo | Tarea | Horas |
|---|---|---:|
| **Técnica** | **T4 · Caché y dequeues en `/ES/`.** Localizar el origen de `Cache-Control: no-store` (candidatos: sesión WooCommerce, plugin `booked`, exclusión de NitroPack) y eliminarlo. Ampliar la condición de los dequeues de las Fases 1-4 a las rutas `/ES/`. Objetivo: 24 → 10 bundles, 64 → menos de 30 hojas de estilo. Requiere QA visual de 6 páginas ES. | 6 h |
| On-Page | **O7 · Consolidar duplicados EN.** Dejar `/eb-5-blog/` como archivo canónico y redirigir `/blog/` y `/category/blog/`. Sacar del sitemap `/midtown-pharr/` y `/brownsville-parkside/`. Decidir entre `/contact-us/` y `/lp-contact-us/` (mismo título y contenido). | 3 h |
| On-Page | **O8 · `llms.txt` + robots + schema.** Actualizar `llms.txt` (fechado 14 Jun, sin URLs ES, sin la aprobación I-956F de Midtown Pharr). Restituir el bloque de AI crawlers en `robots.txt` vía filtro `robots_txt` del tema. Añadir el nodo `Organization` que falta en la home ES. | 2 h |

**Verificación:** `curl -I` sobre `/ES/` muestra caché activo; conteo de assets al nivel del inglés.

### Resultado esperado al cierre de Fase 1

- Cero enlaces rotos en las 215 URLs
- ~40 páginas ES declaradas en sitemap y con idioma correcto
- hreflang recíproco entre idiomas
- Sitio ES cacheado y con la mitad de peso
- **Score estimado: 78/100**

---

## 3. Fase 2 — Profundidad de contenido y E-E-A-T

**Duración:** semanas 5-10 · **Esfuerzo:** ~60 horas

- **Páginas de país.** Llevar las 18 páginas cortas (10 ES + 8 EN) a 400-600 palabras con contenido específico de mercado.
- **Países faltantes.** Crear Canadá, Francia, Turquía y Venezuela en ambos idiomas (hoy enlazadas desde el menú y devolviendo 404).
- **Señales de autoría.** Biografías de autor con `Person` schema en las entradas de blog. Requisito en sector YMYL de inmigración e inversión.
- **Guía pilar.** Reescritura de `/the-complete-guide-to-eb-5-investment/` y su equivalente español con estructura de preguntas y respuestas.
- **Datos de schema.** Integrar los 11 datos pendientes del cliente para habilitar Knowledge Panel.
- **Cabeceras de seguridad.** HSTS, CSP, X-Frame-Options, COOP.

---

## 4. Fase 3 — Autoridad y visibilidad

**Duración:** semanas 11-20 · **Esfuerzo:** ~80 horas

El problema de fondo: 4 keywords orgánicas y 1 visita al mes. El sitio está técnicamente sano pero es invisible. **Sin enlaces entrantes no hay competencia posible en EB-5.**

- **Presencia en terceros.** Directorios del sector (IIUSA, EB5 Investors, plataformas de Regional Centers) y medios de inmigración en mercados hispanos.
- **Calendario editorial.** Contenido en español enfocado en México, Chile, Argentina y España, donde ya hay posiciones.
- **Optimización para buscadores con IA.** Formato de respuesta directa y cápsulas de citación, aprovechando que `llms.txt` y el schema ya están en su sitio.
- **Limpieza de enlaces.** Revisión y disavow de los 94 dominios señalados en Search Console.
- **Medición.** Informe mensual de posiciones por mercado y por idioma.

---

## 5. Entregables

| Fase | Entregable | Formato | Cuándo |
|---|---|---|---|
| 1 | Paquetes de tema con manifiesto MD5 e instrucciones de subida | ZIP + Markdown | Semanal |
| 1 | Re-crawl de verificación de las 215 URLs | CSV + panel | Fin semana 4 |
| 1 | Hoja de títulos y meta descriptions para cargar en Yoast | Hoja de cálculo | Semanas 1-3 |
| 2 | Contenido de páginas de país en ambos idiomas | Markdown + carga | Semanas 5-10 |
| 2 | Guía pilar reescrita, EN y ES | Markdown + carga | Semana 9 |
| 3 | Informe mensual de posiciones por mercado | Panel + PDF | Mensual |

---

## 6. Dependencias del cliente

| Elemento | Bloquea | Urgencia |
|---|---|---|
| Acceso al panel de NitroPack | Combine JS, Delay JS, Critical CSS, caché ES | Semana 1 |
| Acceso a cPanel | Reglas 301, apagado de AccelerateWP | Semana 2 |
| Los 11 datos de schema (RC ID USCIS, dirección, teléfono E.164, email, año, áreas, idiomas) | Knowledge Panel y rich results | Fase 2 |
| Logo cuadrado 200×200 o mayor | Knowledge Panel (el actual es 674×150) | Fase 2 |
| Biografías y credenciales del equipo | Señales E-E-A-T en sector YMYL | Fase 2 |
| Validación legal del contenido nuevo | Publicación de páginas de país | Continuo |

---

## 7. Condiciones de trabajo

El sitio se despliega **únicamente por FTP y sin entorno de staging**, y hubo un incidente de corrupción de archivos en una transferencia previa (julio de 2026). Por eso:

- Todo cambio de plantilla se entrega como **paquete comprimido con manifiesto MD5**, para extraer vía cPanel File Manager y verificar tras la subida.
- No se suben archivos `.php` sueltos por FTP.
- Los cambios de configuración de NitroPack, cPanel y Yoast dependen de acceso del cliente.

---

## 8. Expectativas de plazo

Las Fases 1 y 2 corrigen problemas que hoy impiden competir, y su efecto se ve en **indexación e impresiones en cuestión de semanas**.

El crecimiento de posiciones y tráfico depende de la Fase 3, que es trabajo de autoridad con **horizonte de tres a seis meses**. Prometer movimiento de rankings en 30 días en un sector YMYL con la autoridad actual del dominio no sería realista.
