# Multiplexador de archivos MKV con `mkvmerge`

Este script busca recursivamente archivos `.mkv` dentro de la carpeta donde se ejecuta y sus subcarpetas, y permite multiplexarlos usando `mkvmerge.exe`. Los archivos multiplexados se guardan en la misma carpeta que el original con el sufijo `_multiplexado.mkv` para evitar conflictos.

------------------------------------------------------------------------------------------------------------

## Requisitos

* Python 3.x
_____________________________________________
* `tqdm` (barra de progreso). Instalar con:
                                          
 ```                                       
 pip install tqdm                          
 ```                                       
---------------------------------------------
* `mkvmerge.exe` debe estar en la misma carpeta donde se ejecuta el script o empaquetado con PyInstaller.

----------------------------------------------------------------------------------------------------------

## Funcionalidades principales

* **Búsqueda recursiva:** El script explora todas las subcarpetas para encontrar archivos `.mkv`.
* **Selección de archivos:** Puedes multiplexar todos los archivos encontrados o seleccionar individualmente cuáles procesar.
* **Multiplexado con progreso:** Utiliza `mkvmerge` para multiplexar cada archivo mostrando una barra de progreso basada en el porcentaje reportado por `mkvmerge`.
* **Evitación de conflictos:** Los archivos multiplexados se guardan con el sufijo `_multiplexado.mkv` en la misma carpeta que el archivo original.
* **Compatibilidad con PyInstaller:** Soporta ejecución desde un ejecutable creado con PyInstaller, buscando `mkvmerge.exe` en la carpeta temporal `_MEIPASS`.

-------------------------------------------------------------------------------------------------------------

## Uso

1. Coloca `mkvmerge.exe` en la carpeta del script o en la carpeta de ejecución.
2. Ejecuta el script (o el ejecutable generado).
3. El script buscará todos los archivos `.mkv` en la carpeta actual y sus subcarpetas.
4. Se mostrará un menú para elegir multiplexar todos o solo algunos archivos.
5. Se procesarán los archivos seleccionados mostrando la barra de progreso.
6. Los archivos multiplexados se guardarán junto al original con sufijo `_multiplexado.mkv`.

-------------------------------------------------------------------------------------------------------------

## Código (breve descripción)

* `obtener_rutas()`: Devuelve la carpeta actual.
* `buscar_archivos_mkv(input_folder)`: Busca recursivamente archivos `.mkv`.
* `obtener_mkvmerge_path()`: Detecta la ruta de `mkvmerge.exe`, compatible con PyInstaller.
* `multiplexar_archivo()`: Ejecuta `mkvmerge` para multiplexar con barra de progreso.
* `mostrar_menu_y_elegir()`: Muestra el menú para seleccionar archivos.
* `main()`: Lógica principal que coordina las funciones anteriores.

-------------------------------------------------------------------------------------------------------------

## Notas

* El script asume que `mkvmerge.exe` puede reportar progreso en la salida estándar, lo que permite actualizar la barra `tqdm`.
* La barra de progreso muestra solo porcentaje, sin velocidad.
* Si `mkvmerge.exe` no se encuentra, el script terminará mostrando un mensaje de error.

-------------------------------------------------------------------------------------------------------------

## script para complilar en windows
#--------------------------------------------------------------------------------------------------------------#
#scrips para compilar con PyInstaller: pyinstaller --onefile --add-binary "mkvmerge.exe;." --icon=ico.ico REMOVEIDMKV_1_00.py
 |
#--------------------------------------------------------------------------------------------------------------#

