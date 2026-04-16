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
- **🕒 Historial de Cálculo**: Registro guardado internamente mediante *SQLite*, lo que mantiene memoria para auditar cálulos previos.

---

## 🏗 Arquitectura del Software (El Esqueleto)

Nuestro objetivo con el código ha sido respetar la **Separación Estricta de Responsabilidades**. Hemos procurado que el motor matemático matemático sea "indiferente" ante la interfaz visual: la interfaz lo dibuja, el motor solo lo resuelve.

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
* **`history_repo.py`**: Intercomunicador simple hacia base de datos SQLite para registros perennes.

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
