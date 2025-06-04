import os
import sys
import subprocess
from tqdm import tqdm
import time
import re

def obtener_rutas():
    input_folder = os.getcwd()
    return input_folder

def buscar_archivos_mkv(input_folder):
    archivos = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".mkv"):
                archivos.append(os.path.join(root, file))
    return archivos

def obtener_mkvmerge_path():
    if hasattr(sys, '_MEIPASS'):
        mkvmerge_path = os.path.join(sys._MEIPASS, "mkvmerge.exe")
    else:
        mkvmerge_path = os.path.join(os.getcwd(), "mkvmerge.exe")
    if not os.path.isfile(mkvmerge_path):
        print(f"❌ No se encontró mkvmerge.exe en {mkvmerge_path}")
        input("Presiona ENTER para salir...")
        sys.exit(1)
    return mkvmerge_path

def multiplexar_archivo(mkvmerge_path, video_path, output_path, forzar_aspecto=False):
    cmd = [
        mkvmerge_path,
        "--no-track-tags",
        "--no-global-tags"
    ]

    if forzar_aspecto:
        cmd += ["--aspect-ratio", "0:16/9"]  # 0 es la primera pista de video por defecto

    cmd += ["-o", output_path, video_path]

    print(f"🛠️ Ejecutando: {' '.join(cmd)}")

    progress_re = re.compile(r'Progress: (\d+)%')

    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) as process:
            pbar = tqdm(total=100, desc=os.path.basename(video_path), ncols=80, unit='%')
            for line in process.stdout:
                line = line.strip()
                match = progress_re.search(line)
                if match:
                    percent = int(match.group(1))
                    pbar.n = percent
                    pbar.refresh()

            pbar.n = 100
            pbar.refresh()
            pbar.close()

            return_code = process.wait()
            if return_code != 0:
                print(f"⚠️ Error: mkvmerge retornó código {return_code}")
    except Exception as e:
        print(f"❌ Error al ejecutar mkvmerge: {e}")

def mostrar_menu_y_elegir(archivos):
    print("\n=== Archivos encontrados ===")
    for idx, archivo in enumerate(archivos, 1):
        print(f"{idx}. {os.path.basename(archivo)}")
    print(f"\nTotal de archivos: {len(archivos)}")
    while True:
        print("\nElija una opción:")
        print("1. Multiplexar TODOS los archivos")
        print("2. Seleccionar archivos individualmente")
        opcion = input("Ingrese su opción (1/2): ").strip()
        if opcion == '1':
            return archivos
        elif opcion == '2':
            seleccionados = []
            print("Ingrese los números de los archivos a multiplexar (separados por comas):")
            nums = input().split(',')
            for num in nums:
                try:
                    idx = int(num.strip()) - 1
                    if 0 <= idx < len(archivos):
                        seleccionados.append(archivos[idx])
                except:
                    pass
            return seleccionados
        else:
            print("❌ Opción inválida. Intente de nuevo.")

def preguntar_aspect_ratio():
    while True:
        opcion = input("\n¿Deseas forzar el aspecto 16:9 (relación 16/9) en los videos? (s/n): ").strip().lower()
        if opcion in ('s', 'n'):
            return opcion == 's'
        else:
            print("❌ Entrada inválida. Escriba 's' o 'n'.")

def main():
    mkvmerge_path = obtener_mkvmerge_path()
    input_folder = obtener_rutas()
    archivos = buscar_archivos_mkv(input_folder)
    if not archivos:
        print("❌ No se encontraron archivos .mkv en la carpeta.")
        input("Presiona ENTER para salir...")
        return
    seleccionados = mostrar_menu_y_elegir(archivos)
    if not seleccionados:
        print("⚠️ No se seleccionaron archivos para multiplexar.")
        input("Presiona ENTER para salir...")
        return
    forzar_aspecto = preguntar_aspect_ratio()
    tiempo_inicio = time.time()
    for archivo in seleccionados:
        carpeta_original = os.path.dirname(archivo)
        nombre_sin_ext = os.path.splitext(os.path.basename(archivo))[0]
        output_file = os.path.join(carpeta_original, f"{nombre_sin_ext}_multiplexado.mkv")
        print(f"\n🔍 Multiplexando {os.path.basename(archivo)}...")
        multiplexar_archivo(mkvmerge_path, archivo, output_file, forzar_aspecto)
    tiempo_total = time.time() - tiempo_inicio
    print(f"\n✅ Multiplexado completado: {len(seleccionados)} archivo(s).")
    print(f"⏱️ Tiempo total: {tiempo_total:.2f} segundos.")
    input("Presiona ENTER para salir...")

if __name__ == "__main__":
    main()
    
#
#------------------------------------------------------------------------------------------------------------------------------#
# scrips para compilar con PyInstaller: pyinstaller --onefile --add-binary "mkvmerge.exe;." --icon=ico.ico REMOVEIDMKV_1_00.py |
#------------------------------------------------------------------------------------------------------------------------------#