# Especificación de Requerimientos  
## Aplicación de Métodos Numéricos en Python

### 1. Propósito

Desarrollar una aplicación de escritorio en Python para resolver problemas de Métodos Numéricos de manera guiada, visual y didáctica. La aplicación permitirá al usuario seleccionar un método, ingresar parámetros mediante formularios asistidos, ejecutar el cálculo, observar el procedimiento paso a paso, consultar tablas de iteraciones, visualizar gráficas, revisar el historial de cálculos y exportar los resultados a PDF.

### 2. Base del proyecto

Este documento se elabora a partir del enunciado del proyecto final, el cual establece como obligatorios los módulos de cálculo de raíces, interpolación y ajuste de curvas, sistemas de ecuaciones, derivación e integración numérica y ecuaciones diferenciales. También exige el uso de Python 3.x, NumPy y Matplotlib, además de una interfaz gráfica desarrollada con una de las opciones permitidas: Tkinter, PyQt, Streamlit o Jupyter Notebook interactivo. El mismo enunciado recomienda una estructura modular, separación entre lógica e interfaz, validaciones de entrada y documentación del sistema. fileciteturn1file0

### 3. Alcance funcional

La aplicación deberá incluir, como mínimo, los siguientes módulos:

#### 3.1 Cálculo de raíces
- Método de Bisección
- Método de Newton-Raphson
- Método de la Secante

#### 3.2 Interpolación y ajuste de curvas
- Interpolación con el polinomio de Lagrange
- Interpolación con el polinomio de Newton
- Visualización de resultados interpolados

#### 3.3 Sistemas de ecuaciones
- Resolución de sistemas lineales por el método de Gauss-Seidel
- Factorización LU

#### 3.4 Derivación e integración numérica
- Aproximación de derivadas por diferencias finitas
- Integración numérica por método del Trapecio
- Integración numérica por método de Simpson

#### 3.5 Ecuaciones diferenciales
- Método de Euler
- Método de Runge-Kutta

Estos módulos coinciden con los requisitos funcionales definidos en el proyecto. fileciteturn1file0

### 4. Decisión de interfaz

La aplicación se propone como una solución de escritorio moderna, visualmente atractiva e intuitiva. Para cumplir con el objetivo de una interfaz “más bonita, intuitiva y responsive”, se recomienda usar **PyQt6** como tecnología principal de interfaz. La aplicación deberá organizarse con:
- un menú lateral para seleccionar el tema central;
- submenús o secciones internas para cada método;
- panel principal dinámico para el formulario, la solución y la gráfica;
- tema claro y tema oscuro;
- diseño adaptable al tamaño de la ventana.

> Nota de diseño: si al desarrollar se detecta que alguna parte de la interfaz requiere mayor rapidez de prototipado, el sistema puede usar componentes nativos de Qt Designer y luego integrarlos en Python.

### 5. Requerimientos funcionales

#### RF-01. Selección de módulo
El sistema deberá permitir al usuario elegir el módulo principal desde un menú lateral.

#### RF-02. Selección de método
Dentro de cada módulo, el sistema deberá mostrar los métodos disponibles para ejecución.

#### RF-03. Captura guiada de datos
Cada método deberá presentar campos guiados con etiquetas claras, ejemplos y restricciones de formato.

#### RF-04. Validación de entradas
El sistema deberá validar tipo de dato, valores nulos, intervalos inválidos, tolerancias, cantidades de puntos, dimensiones compatibles y cualquier otro parámetro requerido por el método.

#### RF-05. Ejecución del algoritmo
El sistema deberá ejecutar el método seleccionado con los datos ingresados por el usuario.

#### RF-06. Desglose paso a paso
El sistema deberá mostrar el procedimiento matemático de manera progresiva, no solo el resultado final.

#### RF-07. Tabla de iteraciones
El sistema deberá generar una tabla de iteraciones para cada método, o una tabla equivalente cuando el método no sea iterativo.

#### RF-08. Gráfica de resultados
El sistema deberá mostrar una gráfica relacionada con el método ejecutado cuando aplique.

#### RF-09. Exportación a PDF
El sistema deberá exportar el resultado completo a PDF, incluyendo:
- datos ingresados,
- procedimiento,
- tabla de iteraciones,
- resultado final,
- observaciones,
- gráfica incrustada cuando corresponda.

#### RF-10. Historial de cálculos
El sistema deberá guardar el historial de operaciones realizadas por el usuario.

#### RF-11. Ejemplos precargados
El sistema deberá incluir ejemplos precargados por método para facilitar el uso a personas sin experiencia.

#### RF-12. Tema oscuro
El sistema deberá permitir activar y desactivar un tema oscuro.

#### RF-13. Reutilización de resultados
El sistema deberá permitir consultar un cálculo anterior desde el historial y volver a ejecutarlo o editar sus parámetros.

#### RF-14. Guía al usuario
La aplicación deberá incluir textos de ayuda, descripciones y ejemplos en pantalla para orientar al usuario durante el uso.

### 6. Requerimientos por módulo

#### 6.1 Módulo de cálculo de raíces

##### Métodos
- Bisección
- Newton-Raphson
- Secante

##### Entradas mínimas
- Función f(x)
- Intervalo inicial o valor inicial, según el método
- Tolerancia
- Número máximo de iteraciones

##### Salidas mínimas
- Raíz aproximada
- Error aproximado
- Número de iteraciones
- Historial de iteraciones
- Gráfica de la función y, cuando aplique, de la convergencia

##### Tabla de iteraciones sugerida
**Bisección**
| No. | a | c = Xm | b | f(a) | f(c) | f(b) | Error |
|---|---:|---:|---:|---:|---:|---:|---:|

**Newton-Raphson**
| Iteración | xn | f(xn) | f´(xn) | xn+1 | f(xn+1) | e |
|---|---:|---:|---:|---:|---:|---:|

**Secante**
| Iteración | xn-1 | xn | f(xn-1) | f(xn) | xn+1 | e |
|---|---:|---:|---:|---:|---:|---:|

##### Reglas del módulo
- El método de Bisección solo deberá ejecutarse si existe cambio de signo en el intervalo.
- Newton-Raphson deberá requerir derivada explícita o derivación simbólica asistida.
- Secante deberá utilizar dos valores iniciales distintos.
- En todos los casos se deberá detener la iteración si se alcanza la tolerancia o el máximo de iteraciones.

#### 6.2 Módulo de interpolación y ajuste de curvas

##### Métodos
- Lagrange
- Newton

##### Entradas mínimas
- Lista de puntos x
- Lista de puntos y
- Valor o vector de interpolación

##### Salidas mínimas
- Polinomio interpolante
- Valor interpolado
- Tabla de diferencias o coeficientes
- Gráfica de puntos originales y curva interpolada

##### Tabla de iteraciones o desarrollo sugerida
**Lagrange**
| i | xi | yi | Li(x) | Término | Acumulado |
|---|---:|---:|---:|---:|---:|

**Newton**
| i | xi | yi | Diferencia dividida | Coeficiente | Acumulado |
|---|---:|---:|---:|---:|---:|

##### Reglas del módulo
- El usuario no podrá ingresar puntos repetidos en x.
- La cantidad de puntos debe ser mayor o igual a 2.
- La curva interpolada deberá representarse en un rango adecuado respecto a los datos ingresados.

#### 6.3 Módulo de sistemas de ecuaciones

##### Métodos
- Gauss-Seidel
- Factorización LU

##### Entradas mínimas
- Matriz de coeficientes
- Vector independiente
- Tolerancia
- Máximo de iteraciones
- Vector inicial, cuando aplique

##### Salidas mínimas
- Vector solución
- Número de iteraciones o proceso de factorización
- Error o residuo final
- Historial de iteraciones
- Verificación del sistema, si corresponde

##### Tabla de iteraciones sugerida
**Gauss-Seidel**
| Iteración | x1 | x2 | x3 | ... | Error |
|---|---:|---:|---:|---:|---:|

**LU**
| Paso | Operación | Matriz L | Matriz U | Observación |
|---|---|---|---|---|

##### Reglas del módulo
- El sistema deberá validar compatibilidad de dimensiones.
- En Gauss-Seidel deberá alertar cuando la matriz no sea diagonalmente dominante o cuando la convergencia no esté garantizada.
- En LU deberá mostrar descomposición paso a paso cuando sea posible.

#### 6.4 Módulo de derivación e integración numérica

##### Métodos
- Diferencias finitas
- Trapecio
- Simpson

##### Entradas mínimas
- Función o tabla de datos
- Intervalo de evaluación
- Número de subintervalos, cuando aplique
- Paso h, cuando aplique

##### Salidas mínimas
- Aproximación numérica
- Desarrollo del método
- Tabla de cálculo
- Gráfica comparativa, si aplica

##### Tabla de iteraciones sugerida
**Diferencias finitas**
| No. | xi | f(xi) | f(xi+h) | Aproximación | Error |
|---|---:|---:|---:|---:|---:|

**Regla del Punto Medio**
| No. | Xi | Xi + 1 | x̄ | f(x̄) | Area (Ai) |
|---|---:|---:|---:|---:|---:|

**Regla Trapezoidal**
| No. | Δx | Xi | f(xi) | factor | Δx/2 * factor * f(xi) |
|---|---:|---:|---:|---:|---:|

**Regla de Simpson**
| No. | △x | Xi | f(xi) | factor | (△x/3) * factor * f(xi) |
|---|---:|---:|---:|---:|---:|

##### Reglas del módulo
- Simpson deberá validar que el número de subintervalos sea par.
- Trapecio y punto medio deberán aceptar tanto función analítica como tabla discreta.
- Las tablas deberán mostrar contribución parcial y acumulada.

#### 6.5 Módulo de ecuaciones diferenciales

##### Métodos
- Euler
- Runge-Kutta

##### Entradas mínimas
- Ecuación diferencial dy/dx = f(x, y)
- Condición inicial
- Intervalo de integración
- Paso h o número de pasos

##### Salidas mínimas
- Solución aproximada
- Tabla de iteraciones
- Curva aproximada
- Comparación entre valores calculados y evolución numérica

##### Tabla de iteraciones sugerida
**Euler**
| Iteración | xi | yi | f(xi, yi) | yi+1 | Error |
|---|---:|---:|---:|---:|---:|

**Runge-Kutta**
| Iteración | xi | yi | k1 | k2 | k3 | k4 | yi+1 | Error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|

##### Reglas del módulo
- El paso h deberá ser positivo y mayor que cero.
- El usuario deberá poder visualizar la evolución punto por punto.
- La gráfica deberá mostrar la aproximación numérica de la solución.

### 7. Requerimientos de interfaz de usuario

#### RI-01. Menú lateral
La aplicación deberá contar con un menú lateral fijo o colapsable para navegar por módulos y métodos.

#### RI-02. Vista central dinámica
La vista principal deberá cambiar según el método seleccionado.

#### RI-03. Diseño moderno
La interfaz deberá usar tipografía clara, espaciado uniforme, tarjetas o paneles, iconografía simple y colores sobrios.

#### RI-04. Modo oscuro
La aplicación deberá incluir un interruptor visible para alternar entre tema claro y oscuro.

#### RI-05. Mensajes de ayuda
Cada formulario deberá mostrar una breve explicación de qué se debe ingresar.

#### RI-06. Botones de acción
Cada pantalla deberá incluir al menos:
- Calcular
- Limpiar
- Cargar ejemplo
- Exportar PDF
- Ver historial

#### RI-07. Resultados organizados
Los resultados deberán mostrarse en secciones separadas:
- resumen,
- procedimiento,
- tabla,
- gráfica,
- observaciones.

### 8. Requerimientos técnicos

#### RT-01. Lenguaje
La aplicación deberá desarrollarse en Python 3.x.

#### RT-02. Librerías obligatorias
- NumPy
- Matplotlib

#### RT-03. Librerías opcionales
- SciPy
- SymPy

#### RT-04. Arquitectura modular
El sistema deberá dividirse en módulos independientes por tema y por responsabilidad.

#### RT-05. Separación de capas
La lógica numérica deberá mantenerse separada de la interfaz de usuario.

#### RT-06. Código escalable
La estructura deberá permitir agregar nuevos métodos en el futuro sin reescribir todo el sistema.

#### RT-07. Manejo de errores
El sistema deberá capturar errores de entrada, de cálculo y de visualización con mensajes comprensibles.

#### RT-08. Persistencia de historial
El sistema deberá guardar el historial de cálculos en un archivo local o base de datos ligera.

### 9. Requerimientos no funcionales

#### RNF-01. Usabilidad
La aplicación deberá poder ser utilizada por personas sin conocimientos técnicos avanzados.

#### RNF-02. Claridad
Los nombres de botones, campos y mensajes deberán ser en español claro.

#### RNF-03. Rendimiento
La aplicación deberá responder rápidamente para conjuntos de datos pequeños y medianos.

#### RNF-04. Mantenibilidad
El código deberá estar organizado en funciones y clases con nombres descriptivos.

#### RNF-05. Portabilidad
La aplicación deberá poder ejecutarse en Windows, Linux o macOS, sujeto a compatibilidad de bibliotecas.

#### RNF-06. Reproducibilidad
Los ejemplos precargados deberán producir resultados consistentes y verificables.

### 10. Casos de uso

#### CU-01. Ejecutar un método de raíces
**Actor:** Usuario final  
**Objetivo:** Encontrar la raíz aproximada de una función.  
**Flujo básico:** El usuario selecciona el método, carga un ejemplo o ingresa una función, establece parámetros, presiona calcular y visualiza el resultado con iteraciones y gráfica.

#### CU-02. Interpolar datos
**Actor:** Usuario final  
**Objetivo:** Estimar valores intermedios a partir de datos conocidos.  
**Flujo básico:** El usuario ingresa o carga puntos, selecciona Lagrange o Newton y obtiene el polinomio, la tabla y la curva interpolada.

#### CU-03. Resolver un sistema lineal
**Actor:** Usuario final  
**Objetivo:** Obtener el vector solución de un sistema de ecuaciones.  
**Flujo básico:** El usuario ingresa la matriz y el vector independiente, elige Gauss-Seidel o LU y recibe el proceso y el resultado.

#### CU-04. Calcular derivada o integral numérica
**Actor:** Usuario final  
**Objetivo:** Aproximar una derivada o una integral con datos o funciones.  
**Flujo básico:** El usuario selecciona el método, ingresa datos, calcula y compara el resultado en tabla y gráfica.

#### CU-05. Resolver una ecuación diferencial
**Actor:** Usuario final  
**Objetivo:** Aproximar la solución de una EDO.  
**Flujo básico:** El usuario escribe la ecuación, coloca la condición inicial y observa la evolución numérica.

#### CU-06. Exportar un reporte
**Actor:** Usuario final  
**Objetivo:** Guardar el cálculo en PDF.  
**Flujo básico:** Tras calcular, el usuario pulsa exportar y obtiene un documento con los datos, procedimiento y resultados.

### 11. Reglas de negocio

#### RB-01
No se permitirá calcular Bisección si el intervalo no encierra una raíz.

#### RB-02
No se permitirá Simpson si la cantidad de subintervalos no es par.

#### RB-03
No se permitirán valores vacíos en campos obligatorios.

#### RB-04
No se permitirán entradas no numéricas en campos exclusivamente numéricos.

#### RB-05
No se permitirán matrices no cuadradas cuando el método lo requiera.

#### RB-06
No se permitirá exportar a PDF si aún no existe un cálculo válido.

#### RB-07
El historial deberá almacenar fecha, hora, método, parámetros y resultado resumido.

#### RB-08
Los ejemplos precargados deberán poder restaurarse en un clic.

#### RB-09
La aplicación deberá mostrar una advertencia cuando el método seleccionado no garantice convergencia.

#### RB-10
Cada cálculo deberá poder reiniciarse sin cerrar la aplicación.

### 12. Criterios de aceptación

#### CA-01
El usuario puede seleccionar cualquier módulo desde el menú lateral.

#### CA-02
Cada método abre su formulario propio con campos guiados.

#### CA-03
Los datos inválidos generan mensajes claros y no bloquean la aplicación.

#### CA-04
Cada cálculo muestra resultado numérico, tabla de iteraciones y gráfica cuando aplique.

#### CA-05
Bisección, Newton-Raphson y Secante muestran evolución iterativa completa.

#### CA-06
Lagrange y Newton muestran el proceso de interpolación y la curva resultante.

#### CA-07
Gauss-Seidel y LU muestran proceso y solución final.

#### CA-08
Trapecio, Simpson, diferencias finitas, Euler y Runge-Kutta muestran tablas de desarrollo.

#### CA-09
El PDF exportado contiene los datos del usuario, procedimiento, tabla, resultado y gráfica.

#### CA-10
El usuario puede cambiar entre tema claro y tema oscuro.

#### CA-11
El usuario puede consultar el historial de cálculos anteriores.

#### CA-12
La aplicación incluye ejemplos precargados funcionales para cada módulo.

### 13. Entregables esperados

El sistema completo deberá producir:
- código fuente organizado por módulos;
- manual de usuario en PDF;
- manual técnico en PDF;
- presentación en PDF o PowerPoint;
- ejecutable opcional;
- archivo comprimido .zip para entrega.

El enunciado también especifica la nomenclatura sugerida para los archivos de entrega y la necesidad de documentación técnica y de usuario. fileciteturn1file1turn1file4turn1file6

### 14. Estructura recomendada del proyecto

```text
proyecto_metodos_numericos/
├── app.py
├── requirements.txt
├── README.md
├── assets/
├── modules/
│   ├── raices/
│   ├── interpolacion/
│   ├── sistemas/
│   ├── integracion_derivacion/
│   └── edos/
├── ui/
│   ├── main_window.py
│   ├── themes.py
│   └── components/
├── services/
│   ├── pdf_export.py
│   ├── history.py
│   └── validators.py
└── tests/
```

### 15. Observaciones de diseño para desarrollo

- Se recomienda que cada método tenga su propia clase o servicio.
- Las funciones numéricas deben ser reutilizables y testeables.
- La interfaz no debe contener lógica matemática compleja.
- El historial y la exportación PDF deben funcionar sin depender de la sesión actual.
- Los ejemplos precargados deben servir como guía para usuarios principiantes.
- La aplicación debe dar prioridad a la claridad del cálculo antes que a una estética recargada.

### 16. Resumen de intención del producto

La aplicación debe sentirse como una herramienta académica moderna, fácil de usar por cualquier persona, con navegación clara, formularios asistidos, resultados bien presentados y trazabilidad completa del proceso matemático. Debe ser útil tanto para aprendizaje como para resolución de ejercicios, manteniendo una base sólida para crecer con nuevos métodos en el futuro.

