@echo off
chcp 65001 >nul
title ViTour Coquimbo - Turismo y Gastronomia
color 0F

echo ================================================================
echo           ViTour Coquimbo - Portal Turistico y Gastronomico
echo ================================================================
echo.

:: 1. Detectar Python
set "PY_CMD=python"
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] No se encontro Python en este equipo.
        echo.
        echo Para usar este proyecto necesitas tener Python instalado:
        echo 1. Descargalo desde: https://www.python.org/downloads/
        echo 2. IMPORTANTE: Marca la casilla "Add python.exe to PATH" al instalar.
        echo.
        pause
        exit /b 1
    )
    set "PY_CMD=py"
)

echo [OK] Python detectado correctamente.
echo.

:: 2. Ir a la carpeta del proyecto
cd /d "%~dp0"

:: 3. Verificar o crear entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Creando entorno virtual .venv...
    %PY_CMD% -m venv .venv
)

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
    set "RUN_PY=python"
) else (
    echo [AVISO] Se utilizara la instalacion directa de Python.
    set "RUN_PY=%PY_CMD%"
)

echo.
echo [2/3] Verificando e instalando librerias Django y Requests...
%RUN_PY% -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [AVISO] Instalando dependencias individualmente...
    %RUN_PY% -m pip install django requests --quiet
)

echo.
echo [3/3] Iniciando el servidor local y abriendo el navegador...
echo.

:: Abrir el navegador tras 3 segundos
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8000/"

echo ================================================================
echo   Servidor activo correctamente en:
echo   - http://127.0.0.1:8000/
echo   - http://127.0.0.1:8000/gastronomia/
echo.
echo   Para cerrar la aplicacion presiona Ctrl + C o cierra esta ventana.
echo ================================================================
echo.

%RUN_PY% manage.py runserver 127.0.0.1:8000

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] El servidor se detuvo o encontro un problema.
    pause
)
