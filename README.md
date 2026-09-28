

## 1. Descripción del Proyecto y Contexto
**ViTour Coquimbo** es una plataforma web desarrollada con **Django Framework** y **MariaDB / MySQL**, orientada a promover y difundir el patrimonio cultural, gastronómico y los destinos turísticos imperdibles de la Región de Coquimbo (La Serena, Coquimbo, Vicuña, Paihuano, Valle del Elqui y Punta de Choros).

En esta segunda etapa evaluativa (**Evaluación Sumativa #2**), la solución evolucionó desde el prototipo inicial basado en archivos JSON hacia una arquitectura profesional con:
- **Persistencia de datos relacional** completa.
- **Modelado avanzado con Django ORM** (relaciones de clave foránea `ForeignKey`).
- **Panel de administración Django Admin** totalmente operativo y personalizado con estilo glassmorphism.
- **Gestión segura de credenciales** a través de variables de entorno (`.env`).
- **Despliegue en producción en la nube** utilizando una instancia **Amazon EC2 (Linux)** en **AWS**.
- **Control de versiones** colaborativo en GitHub.
- **Visualización Front End** dinámica consultando directamente la base de datos y controles visuales para futuras operaciones CRUD.

---

## 2. Arquitectura de la Solución

El proyecto sigue el patrón de arquitectura **MVT (Model-View-Template)** característico de Django:

```text
turismo-region-django/
├── turismo_region/         # Configuración central del proyecto (settings, urls, wsgi)
├── lugares_turisticos/     # Módulo de atractivos y destinos turísticos
│   ├── models.py          # Modelos: Categoria, Ciudad, Lugar
│   ├── views.py           # Vistas basadas en Django ORM y consumo de API Open-Meteo
│   ├── admin.py           # Configuración de administración, filtros y búsquedas
│   └── migrations/        # Historial de migraciones del esquema
├── gastronomia/           # Módulo de recetas tradicionales y gastronomía regional
│   ├── models.py          # Modelos: Categoria, Plato, Ingrediente, PasoPreparacion
│   ├── views.py           # Vistas de catálogo y detalle consultando ORM
│   ├── admin.py           # Administración con TabularInlines para pasos e ingredientes
│   └── migrations/        # Historial de migraciones del esquema
├── templates/             # Plantillas HTML con Bootstrap 5
│   ├── base.html          # Layout principal responsivo
│   ├── admin/             # Personalización visual del panel Django Admin
│   ├── lugares_turisticos/# Vistas del catálogo turístico
│   └── gastronomia/       # Vistas del catálogo gastronómico
├── static/                # Archivos estáticos (CSS personalizado, JS, imágenes)
├── staticfiles/           # Archivos estáticos recopilados (collectstatic)
├── .env.example           # Plantilla de variables de entorno seguras
├── .gitignore             # Exclusión de archivos sensibles y temporales
├── requirements.txt       # Dependencias del proyecto
└── manage.py              # Gestor de comandos de Django
```

---

## 3. Modelo de Datos y Relaciones (Django ORM)

La información histórica almacenada en archivos JSON se migró a un modelo relacional en **MariaDB 10.5**:

### Módulo `lugares_turisticos`
1. **`Categoria`**: Clasificación del atractivo (Playas, Observatorios, Valles, Monumentos).
2. **`Ciudad`**: Comunas de la IV Región (La Serena, Coquimbo, Vicuña, Paihuano, La Higuera).
3. **`Lugar`**: Entidad central con llaves foráneas (`ForeignKey`) hacia `Categoria` y `Ciudad`, campos para descripción, horarios, tarifas, geolocalización (lat/lon) y estado destacado.

### Módulo `gastronomia`
1. **`Categoria`**: Clasificación gastronómica (Platos Marinos, Coctelería, Postres, etc.).
2. **`Plato`**: Entidad principal con `ForeignKey` a `Categoria`, tiempo de preparación, dificultad, porciones y maridaje.
3. **`Ingrediente`**: Relación 1:N con `Plato` (`ForeignKey(Plato, related_name='ingredientes')`).
4. **`PasoPreparacion`**: Relación 1:N con `Plato` (`ForeignKey(Plato, related_name='pasos')`), ordenado por correlativo de paso.

---

## 4. Requerimientos Técnicos y de Infraestructura (AWS EC2)

La aplicación se ejecuta de manera continua en la nube de **Amazon Web Services (AWS)**:

- **Instancia:** Amazon EC2 `t2.micro` / `t3.micro`
- **Sistema Operativo:** Amazon Linux 2023 (Linux Kernel 6.1)
- **Servidor de Base de Datos:** MariaDB 10.5 (`turismo_serena_db`)
- **Gestor Web:** phpMyAdmin 5.2.3 vía Apache (`httpd`) y PHP 8.5
- **Servicio Backend:** Django Framework ejecutándose con entorno virtual (`venv`) y administrado por `systemd` (`django.service`).
- **Variables de Entorno:** Integradas con `python-dotenv` para salvaguardar `SECRET_KEY`, credenciales de base de datos (`DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, `DB_PORT`) y `DEBUG`.

---

## 5. Panel de Administración Django Admin

El panel de administración se encuentra disponible en `/admin/` con diseño dark purple glassmorphic y cuenta con:
- **CRUD completo** sobre todas las entidades: creación, visualización, modificación y eliminación de registros.
- **Búsqueda por texto:** campos `search_fields` en todos los modelos.
- **Filtros laterales dinámicos:** `list_filter` por categoría, ciudad, dificultad y destacados.
- **Edición rápida inline:** `list_editable` y formularios tabulares (`TabularInline`) para ingredientes y pasos de recetas.

---

## 6. Front End y Controles CRUD de Navegación

En las vistas públicas de listado (`/lugares/` y `/gastronomia/`):
- Los datos se obtienen en tiempo real mediante consultas optimizadas de **Django ORM** (`select_related`, `prefetch_related`, `filter`, `Q`).
- Los registros se presentan mediante tarjetas interactivas de **Bootstrap 5**.
- Cada módulo incorpora visualmente los controles para futuras operaciones CRUD:
  - **Botón Buscar:** Formulario de filtrado reactivo por término y categoría.
  - **Botón Agregar:** Botón destacado en el encabezado del catálogo.
  - **Botón Modificar:** Control individual en cada tarjeta de destino o plato.
  - **Botón Eliminar:** Control individual de eliminación en cada tarjeta.

---

## 7. Instrucciones de Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/cris44991/turismo-region-django.git
   cd turismo-region-django
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv .venv
   # En Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # En Linux / macOS:
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (`.env`):**
   ```ini
   SECRET_KEY=tu-clave-secreta-segura
   DEBUG=True
   ALLOWED_HOSTS=*
   DB_NAME=turismo_serena_db
   DB_USER=root
   DB_PASSWORD=tu_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Iniciar servidor:**
   ```bash
   python manage.py runserver
   ```
   Acceder a: `http://127.0.0.1:8000/` y al administrador en `http://127.0.0.1:8000/admin/`.
