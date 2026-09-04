import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo_region.settings')
django.setup()

from django.test import Client
from lugares_turisticos.views import cargar_datos_lugares
from gastronomia.views import cargar_datos_gastronomia

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'docs')
REPO_NAME = 'turismo-region-django'
PREFIX = f'/{REPO_NAME}'

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Copiar archivos estáticos a docs/static
static_src = os.path.join(BASE_DIR, 'static')
static_dst = os.path.join(OUTPUT_DIR, 'static')
shutil.copytree(static_src, static_dst)

# Crear archivo .nojekyll para GitHub Pages
with open(os.path.join(OUTPUT_DIR, '.nojekyll'), 'w') as f:
    pass

client = Client()

def fix_html_urls(content_str):
    # Reemplazar rutas absolutas para que apunten al subdirectorio del repositorio en GitHub Pages
    content_str = content_str.replace('href="/static/', f'href="{PREFIX}/static/')
    content_str = content_str.replace('src="/static/', f'src="{PREFIX}/static/')
    content_str = content_str.replace('href="/lugares/', f'href="{PREFIX}/lugares/')
    content_str = content_str.replace('href="/gastronomia/', f'href="{PREFIX}/gastronomia/')
    content_str = content_str.replace('href="/"', f'href="{PREFIX}/"')
    content_str = content_str.replace("href='/'", f"href='{PREFIX}/'")
    return content_str

def save_page(url_path, output_rel_path):
    response = client.get(url_path)
    if response.status_code == 302:
        # Redirección
        target = response.url
        response = client.get(target)
    
    html_content = response.content.decode('utf-8')
    html_content = fix_html_urls(html_content)
    
    file_path = os.path.join(OUTPUT_DIR, output_rel_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Exportado: {url_path} -> docs/{output_rel_path}")

# 1. Página principal / Lugares
save_page('/lugares/', 'index.html')
save_page('/lugares/', 'lugares/index.html')

# 2. Detalles de lugares
lugares = cargar_datos_lugares()
for l in lugares:
    l_id = l['id']
    save_page(f'/lugares/{l_id}/', f'lugares/{l_id}/index.html')

# 3. Gastronomia
save_page('/gastronomia/', 'gastronomia/index.html')

# 4. Detalles de gastronomia
platos = cargar_datos_gastronomia()
for p in platos:
    p_id = p['id']
    save_page(f'/gastronomia/{p_id}/', f'gastronomia/{p_id}/index.html')

print("¡Exportación completada exitosamente en la carpeta docs/!")
