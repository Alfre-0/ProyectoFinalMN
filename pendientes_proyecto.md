# 📋 Lista de Tareas Pendientes del Proyecto

Tras cruzar nuestro avance con la rúbrica oficial (`PROYECTO METODOS NUMÉRICOS.pdf`), he determinado que **hemos cumplido con la gran mayoría de los requisitos**, incluyendo el uso obligatorio de PyQt, SymPy, NumPy y Matplotlib, y la implementación de los Módulos 1, 2, 3 y 5 al completo.

Sin embargo, para garantizar la nota máxima (15/15), aún nos falta completar los siguientes puntos que el PDF especifica claramente:

## 1. ⚙️ Desarrollar "Derivación por Diferencias Finitas"
Según la rúbrica, el **Módulo 4** se llama *"Derivación e Integración Numérica"* y exige explícitamente:
- [ ] Aproximación de derivadas mediante diferencias finitas.
> **Nota:** Anteriormente transformamos esta vista a "Punto Medio" por petición tuya en la interfaz. Necesitamos crear una nueva vista matemática exclusiva de Derivación (Diferencias hacia adelante, atrás o centradas) que comparta espacio con Trapecio y Simpson.

## 2. 📖 Generación de Manuales en Formato PDF
Los "Entregables" oficiales solicitan estrictamente los manuales **en formato PDF** separados por tipo. Aunque ya redactamos muy buenos archivos Markdown (`DOCUMENTACION.md`), necesitamos maquetarlos formalmente en:
- [ ] **Manual de Usuario (PDF):** Con capturas de pantalla, proceso de instalación y guía de uso por pantalla.
- [ ] **Manual Técnico (PDF):** Con explicación de los algoritmos (bisección, newton, etc.), arquitectura del software usando clases y requerimientos de las librerías.

## 3. 📦 Preparación del Paquete de Entrega ZIP
El PDF establece un estándar de nomenclatura riguroso que debes seguir para subirlo a tu plataforma. Faltaría prepararlo:
- [ ] Crear archivo estructurado como `[Carné]_ProyectoFinalMN_Codigo.zip`
- [ ] Asegurarnos de tener los nombres de los PDFs como exigen: `[Carné]_ProyectoFinalMN_ManualUsuario.pdf`, etc.

## 4. 🎦 Presentación (Opcional, pero se evaluará Creatividad)
Te piden uno de estos entregables extra:
- [ ] Diapositivas explicativas (PowerPoint o PDF).
- [ ] **O** un video demostrativo de menos de 5 minutos utilizando los diferentes módulos de nuestra aplicación.

### ¿Qué hacemos primero?
Te sugiero fuertemente que empecemos por programar el punto 1 (**Diferencias Finitas**) ya que toca el código fuente. Una vez que la aplicación esté funcional al 100%, pasamos a tomar capturas y generar un script de Python para armar y exportar hermosos PDFs directamente para tu entrega.

// Bien, continua con la implementación de Derivación por Diferencias Finitas, deja intacto como esta Punto Medio, Trapacio y Simpson, añade ese nuevo módulo donde corresponda.