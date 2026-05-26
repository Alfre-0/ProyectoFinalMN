# 📐 Proyecto Final: Métodos Numéricos

![Carátula/Banner](https://img.shields.io/badge/Estado-Finalizado-success?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white) ![PyQt6](https://img.shields.io/badge/PyQt-6-green?style=for-the-badge&logo=qt)

Bienvenido a la documentación de la aplicación integral de **Métodos Numéricos**. Una plataforma educativa y resolutiva escrita en Python que te permite visualizar matemática interactiva, gráficas dinámicas y procedimientos iterativos de principio a fin de manera fluida.

---

## 🎯 ¿Qué hace esta aplicación?

Es una calculadora avanzada de escritorio con interfaz gráfica (GUI) construida que agrupa distintos métodos numéricos enseñados clásicamente en ingeniería y desarrollo de software numérico. No solo escupe un resultado: **enseña el camino**. Muestra el procedimiento de resolución paso a paso tal en un pizarrón gracias a la estilización algebraica y matemática diseñada a medida.

### ✨ Funcionalidades Principales
- **🧩 Input y Renderizado Matemático**: Interacciones con un potente `MathCanvas` personalizado en lugar de campos de texto plano convencionales. Las ecuaciones lucen algebraicas en tiempo real (por ejemplo $x^2$ y fracciones naturales).
- **📝 Procedimiento a detalle**: Documentación de todo el desarrollo algebraico y lógico. Si pones un método de interpolación, te mostrará la fórmula general, valores de sustitución y desarrollo fraccionario. 
- **📈 Gráficos Interactivos**: Creados sobre **Matplotlib**, permiten a los usuarios acercar e inspeccionar el comportamiento de las funciones visualmente.
- **💾 Reportes en PDF**: ¿Tienes un examen o tarea? Presiona **Exportar PDF** para plasmar un reporte elegante y formateado incluyendo la gráfica resultante, la tabla iterativa y los datos de entrada.
- **🕒 Historial de Cálculo**: Registro guardado internamente mediante un archivo *JSON* local en la carpeta `data/`, lo que mantiene memoria para auditar cálculos previos.

## 🏗 Arquitectura del Software (El Esqueleto)

Nuestro objetivo con el código ha sido respetar la **Separación Estricta de Responsabilidades**. Hemos procurado que el motor matemático matemático sea "indiferente" ante la interfaz visual: la interfaz lo dibuja, el motor solo lo resuelve.

### 📂 Estructura del Proyecto (Solo Código Fuente)

```text
ProyectoFinalMN/
├── main.py                          # Punto de entrada de la aplicación
├── requirements.txt                 # Dependencias del proyecto
├── DOCUMENTACION.md                 # Documentación técnica general
├── GUIA_INSTALACION.md              # Guía de instalación y configuración
├── especificacion_requerimientos_metodos_numericos.md # Especificaciones de la UMG
├── core/                            # Capa de Lógica Matemática (Core)
│   ├── __init__.py
│   ├── edos/
│   │   ├── __init__.py
│   │   └── edos.py                  # Algoritmos de Euler y Runge-Kutta 4
│   ├── integracion_derivacion/
│   │   ├── __init__.py
│   │   └── integracion_derivacion.py # Algoritmos de Simpson, Trapecio y Diferencias Finitas
│   ├── interpolacion/
│   │   ├── __init__.py
│   │   └── interpolacion.py         # Algoritmos de Lagrange y Newton
│   ├── raices/
│   │   ├── __init__.py
│   │   └── raices.py                # Algoritmos de Bisección, Newton-Raphson y Secante
│   └── sistemas/
│       ├── __init__.py
│       └── sistemas.py              # Algoritmos de Gauss-Seidel y Factorización LU
├── ui/                              # Capa de Presentación Gráfica (UI)
│   ├── __init__.py
│   ├── main_window.py               # Ventana principal y enrutador de navegación
│   ├── components/
│   │   ├── __init__.py
│   │   ├── math_ast.py              # Árbol de sintaxis abstracta para matemáticas
│   │   ├── math_canvas.py           # Editor gráfico interactivo
│   │   ├── math_input.py            # Campo de entrada de fórmulas
│   │   └── math_keyboard.py         # Teclado interactivo estilo GeoGebra
│   ├── styles/
│   │   ├── __init__.py
│   │   ├── theme.py                 # Gestor de temas claro/oscuro
│   │   └── tokens.py                # Tokens de diseño (Colores, Spacing, Fuentes)
│   └── views/
│       ├── __init__.py
│       ├── base_method_view.py      # Clase base abstracta de cada vista
│       ├── welcome_view.py          # Pantalla de bienvenida
│       ├── raices_views.py          # Vistas para Bisección, Newton y Secante
│       ├── interpolacion_views.py   # Vistas para Lagrange y Newton
│       ├── sistemas_views.py        # Vistas para Gauss-Seidel y LU
│       ├── integracion_views.py     # Vistas para Trapecio, Simpson y Diferencias Finitas
│       ├── edos_views.py            # Vistas para Euler y RK4
│       └── history_view.py          # Vista del historial de cálculos
├── infrastructure/                  # Capa de Soporte y Servicios (Infraestructura)
│   ├── __init__.py
│   ├── history_repo.py              # Repositorio de persistencia del historial
│   ├── pdf_generator.py             # Generador de reportes PDF (fpdf2)
│   └── plot_widget.py               # Lienzo interactivo de gráficas (Matplotlib)
└── data/                            # Almacenamiento local de persistencia
    └── historial.json               # Historial de cálculos guardados (JSON)
```

La arquitectura se divide en capas (Módulos):

### 1. `core/` (Cerebro Numérico 🧠)
Lógica computacional pura y dura (Matemática). Sin interfaz gráfica, puro Python, Numpy y Sympy para cálculo simbólico. 
* **Raíces de Ecuaciones** (`core/raices/`): Bisección, Newton-Raphson, Secante y Falsa Posición.
* **Integración y Derivación** (`core/integracion_derivacion/`): Regla de Simpson (1/3 y 3/8), Trapecio generalizado y Diferencias finitas.
* **Interpolación** (`core/interpolacion/`): Lagrange y tablas de Diferencias Divididas de Newton.
* **Ecuaciones Diferenciales Ordinarias (EDOs)** (`core/edos/`): Métodos de Euler y Runge-Kutta de cuarto orden (RK4).

### 2. `ui/` (La Cara 🎨)
Construida exquisitamente con PyQt6 integrando un sistema de tokens visuales y *Atomic Design* para mantener el "*Vibe*".
* **`views/`:** Vistas y pantallas (cada método hereda de `BaseMethodView`).
* **`components/`:** Elementos reutilizables y altamente interactivos: nuestro teclado virtual `MathKeyboard` y `MathCanvas`.
* **`styles/`:** Paletas estilizadas, variables semánticas, colores de fallo/éxito integrados y soporte fluido "light/dark node".

### 3. `infrastructure/` (Soporte Fuerte 🛠)
Aquí viven los puentes asombrosos del mundo real y los servicios:
* **`pdf_generator.py`**: Interfaz transitoria construida en `fpdf2` que sabe formatear y renderizar bonitos reportes y sanitiza letras tipo LaTeX para adaptarlas a la fuente base.
* **`plot_widget.py`**: Puente a *Matplotlib* integrado orgánicamente a *PyQt6*.
* **`history_repo.py`**: Intercomunicador simple hacia el archivo local JSON en `data/historial.json` para registros perennes.

### 4. `data/` (Persistencia 💾)
Almacén físico para la persistencia de la aplicación:
* **`historial.json`**: Archivo JSON que almacena el historial estructurado de cálculos y parámetros.

---

## 🚀 Flujo de Ejecución Básico

¿Cómo se comunican las cosas desde que abres el programa interactivo hasta que la magia se da?

1.   Abre **`main.py`** e inicia la aplicación a Pantalla Completa Maximizada, invocando **`MainWindow`**.
2.   Eliges un método numérico desde el menú de navegación izquierdo (Ejemplo: Interpolación de Newton).
3.   Ingresas los datos en el lienzo interactivo `MathInput`. 
4.   Haces click al botón  `Calcular`.
5.   Ese gesto entra a la vista y salta la barrera hacia la capa **`core`** (que no sabe qué botón fue), el Core lo enciende todo y vomita el resultado `InterpolationResult` repleta de datos, iteraciones, gráficas y fórmulas simbólicas limpias, sin multiplicadores inoficiosos (`sympy` custom formatter).
6.   Y ese resultado es interceptado por un QTable, un Panel Lector en `_display_result` y nuestro Canvas que lo visualiza bellísimo finalizando la sesión y activando el PDF.

---

## 📚 Stack Tecnológico Elegido
* **Numpy:** Eficiencia increíble en las matrices matemáticas y vectorizado de los arrays dinámicos para los gráficos de Matplotlib en tiempo real.
* **Sympy:** Nuestro aliado para cálculo simbólico. Nos ayuda a transformar formulas muertas a matemáticas "vivas", manipulables y comprensibles por el código y el usuario (derivadas directas de ecuaciones texto).
* **PyQt6:** La madurez del *framework Qt* provee reactividad sin comprometer el estilo CSS enlazado.
* **Matplotlib:** Cimiento para la generación de gráficas estables y enlazables dentro de elementos nativos OS.

---
> *Creado con las mejores prácticas arquitectónicas: "La UI es inteligente manipulando estados, pero daltónica calculando derivadas."*
