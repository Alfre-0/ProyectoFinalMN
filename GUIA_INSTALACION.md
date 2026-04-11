# Guía de Instalación y Ejecución — Métodos Numéricos

Esta guía detalla los pasos a seguir para configurar, instalar dependencias y ejecutar sin problemas el programa de Métodos Numéricos escrito en Python (PyQt6).

---

## 📌 Requisitos Previos

1. **Python 3.10 o superior**
   - Asegúrate de tener Python instalado en tu PC. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
   - **IMPORTANTE (Windows):** Durante la instalación, marca la casilla que dice **"Add python.exe to PATH"** antes de dar clic en *Install Now*.

2. **Descargar los archivos del proyecto**
   - Ten la carpeta con todos los archivos fuente del proyecto (donde se encuentra el archivo `main.py` y `requirements.txt`).

---

## ⚙️ Pasos de Instalación

Existen dos maneras de instalar las dependencias: globalmente o mediante un entorno virtual recomendado. **Es altamente recomendable utilizar un entorno virtual** para evitar conflictos con otras versiones u otros programas.

### Opción Recomendada (Usando Entorno Virtual)

1. **Abre tu terminal o consola de comandos (CMD, PowerShell o Terminal de VS Code).**
2. **Navega a la carpeta principal del proyecto** (donde está alojado el archivo `main.py`):
   ```bash
   cd "ruta\a\la\carpeta\ProyectoFinalMN"
   ```
3. **Crea un entorno virtual:**
   ```bash
   python -m venv .venv
   ```
4. **Activa el entorno virtual:**
   - En **Windows (CMD):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - En **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   *(Una vez activado, deberías ver `(.venv)` al inicio de tu línea de comandos).*
5. **Instala las librerías necesarias** leyendo el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Cómo Ejecutar el Programa

Una vez finalizada la instalación de los requerimientos, el único comando necesario para abrir la aplicación es:

```bash
python main.py
```

*(Nota: Si usaste un entorno virtual, asegúrate de tenerlo activado siempre que vayas a correr el comando `python main.py`).*

---

## 🛠️ Posibles Errores

- **"pip no se reconoce como un comando interno o externo..."**
  *Causa:* Python no se añadió al PATH durante la instalación.
  *Solución:* Reinstala Python asegurándote de marcar "Add Python to PATH", o agrégalo manualmente en las variables de entorno de Windows.
  
- **Errores de importación (ModuleNotFoundError)**
  *Causa:* Faltó ejecutar la instalación de alguna librería o tu entorno virtual no está activado.
  *Solución:* Vuelve a correr `pip install -r requirements.txt` asegurándote de ver `(.venv)` en la terminal.

- **Falla en terminal con "ejecución de scripts deshabilitada" (Solo PowerShell)**
  *Solución:* Si PowerShell no te deja activar el entorno, abre una nueva ventana de PowerShell como Administrador y escribe:
  `Set-ExecutionPolicy Unrestricted`
  Acéptalo e inténtalo de nuevo.
