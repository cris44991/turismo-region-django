# INFORME TÉCNICO Y REGISTRO DE EVIDENCIAS DE DESARROLLO
## Evaluación Sumativa #1: Archivo de Programa del Lado del Servidor

---


## 1. DESCRIPCIÓN GENERAL DEL PROYECTO

El presente proyecto consiste en el desarrollo de un sitio web modular del lado del servidor construido sobre **Django Framework (Python 3.12)**. Su propósito principal es organizar y difundir información turística y gastronómica de la Región de Coquimbo (La Serena, Coquimbo, Valle de Elqui y Punta de Choros), facilitando la escalabilidad del código mediante una arquitectura desacoplada en dos aplicaciones independientes.

### Características Principales:
1. **Arquitectura Modular:** Compuesta por un proyecto principal (`turismo_region`) y dos aplicaciones independientes (`lugares_turisticos` y `gastronomia`), cada una con su propio archivo `urls.py` vinculado mediante `include()` y vistas funcionales.
2. **Almacenamiento en JSON (Sin Base de Datos):** Toda la información se gestiona desde archivos de datos en formato JSON (`data/lugares.json` y `data/gastronomia.json`), los cuales son leídos, iterados y filtrados en memoria por las vistas.
3. **Librería Externa (`requests`):** Se integró el paquete `requests` para consultar en tiempo real la temperatura y condición climática de La Serena mediante la API meteorológica pública de Open-Meteo.
4. **Interfaz y Archivos Estáticos Locales:** Se implementó Bootstrap 5 de forma 100% local en la carpeta `static/vendor/bootstrap/` (sin dependencias CDN) y una plantilla base reutilizable (`base.html`) con herencia de plantillas.

---

## 2. ESTRUCTURA DE CARPETAS DEL PROYECTO

```text
mati/
├── data/                                 # Datos estructurados en JSON (sin BD)
│   ├── lugares.json                      # Catálogo de destinos, atractivos y coordenadas
│   └── gastronomia.json                  # Catálogo de platos, ingredientes y recetas
├── static/                               # Archivos estáticos locales
│   ├── css/styles.css                    # Hoja de estilos personalizada
│   ├── vendor/bootstrap/                 # Bootstrap 5 local (CSS y JS compilados)
│   └── img/                              # Fotografías locales de lugares y platos
├── templates/                            # Plantillas HTML con herencia
│   ├── base.html                         # Plantilla maestra (Navbar, Footer, contenedor)
│   ├── lugares_turisticos/               # Vistas de la aplicación 1 (lista y detalle)
│   └── gastronomia/                      # Vistas de la aplicación 2 (lista y detalle)
├── turismo_region/                       # Proyecto principal (settings.py, urls.py)
├── lugares_turisticos/                   # Aplicación 1 (views.py, urls.py, apps.py)
├── gastronomia/                          # Aplicación 2 (views.py, urls.py, apps.py)
├── manage.py                             # Script de gestión de comandos Django
├── requirements.txt                      # Dependencias del proyecto (django, requests)
└── Evidencias_Tecnicas_Evaluacion_1.docx # Documento Word formal para entrega
```

---

## 3. EVIDENCIAS DEL USO DE INTELIGENCIA ARTIFICIAL

Durante el desarrollo del proyecto se utilizó Inteligencia Artificial Generativa como herramienta de consulta técnica y apoyo puntual para optimizar aspectos específicos de programación, maquetación responsive y consumo seguro de APIs externas.

---


### Consulta 1: Consumo de API Externa con Timeout y Manejo de Conectividad

#### 📌 Prompt Utilizado:
> *"Para cumplir el requerimiento de usar una librería externa en Django, estoy usando requests para consultar la API meteorológica de Open-Meteo para La Serena. ¿Cuál es el patrón recomendado para fijar un timeout estricto de 3 segundos y retornar datos por defecto en caso de falla de red, evitando que la página tarde en cargar?"*

#### 💡 Recomendación Obtenida:
```python
def obtener_clima_la_serena():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-29.9027&longitude=-71.2519&current=temperature_2m,weather_code"
    try:
        respuesta = requests.get(url, timeout=3)
        if respuesta.status_code == 200:
            datos = respuesta.json().get('current', {})
            return {'disponible': True, 'temperatura': f"{datos.get('temperature_2m')}°C"}
    except Exception:
        pass
    return {'disponible': True, 'temperatura': '19.0°C', 'ciudad': 'La Serena'}
```

#### 🛠️ Incorporación al Código:
Se implementó en `lugares_turisticos/views.py`, garantizando que la aplicación continúe operativa aun en entornos sin conexión a internet durante la evaluación.

---

### Consulta 3: Estilización de Tarjetas Bootstrap 5 con Efecto Hover y Badges

#### 📌 Prompt Utilizado:
> *"¿Cómo estructurar tarjetas con Bootstrap 5 local y CSS personalizado para lograr que las fotos tengan un alto fijo uniforme  flotantes sobre la imagen y un efecto de micro-elevación suave al pasar el mouse?"*

#### 💡 Recomendación Obtenida:
```css
.card-stitch {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.card-stitch:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 30px -10px rgba(15, 23, 42, 0.16);
}
```

#### 🛠️ Incorporación al Código:
Se crearon las clases visuales en `static/css/styles.css` y se aplicaron en las plantillas `templates/lugares_turisticos/lista.html` y `templates/gastronomia/lista.html`.

---

## 4. CONCLUSIONES

El uso de herramientas de Inteligencia Artificial como asistente técnico puntual permitió resolver dudas específicas de sintaxis en Python, buenas prácticas de manejo de excepciones en Django y detalles de maquetación en Bootstrap. El proyecto cumple con la totalidad de los requerimientos establecidos en la pauta de evaluación.
