#!/usr/bin/env python3
"""
Proyecto Final
Autor: Francisco Javier Rojas Santos
Carnet: 202302368

Este programa implementa un menú interactivo para ejecutar los siguientes algoritmos:
1. Prim - Árbol de Expansión Mínima
2. Kruskal - Árbol de Expansión Mínima
3. Dijkstra - Caminos más cortos
4. Huffman - Compresión de texto

Cada algoritmo genera visualizaciones en formato PNG y muestra resultados en consola.

"""

import os
import sys

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.prim import ejecutar_prim
from src.kruskal import ejecutar_kruskal
from src.dijkstra import ejecutar_dijkstra
from src.huffman import ejecutar_huffman


def limpiar_pantalla() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu() -> None:
    """
    Muestra el menú principal del programa.
    Presenta las opciones disponibles al usuario de forma clara y organizada.
    """
    print("\n" + "=" * 60)
    print("       PROYECTO FINAL - ALGORITMOS DE GRAFOS")
    print("=" * 60)
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║                  MENÚ PRINCIPAL                      ║
    ╠══════════════════════════════════════════════════════╣
    ║   0. Salir                                           ║
    ║   1. Ejecutar Prim (MST)                             ║
    ║   2. Ejecutar Kruskal (MST)                          ║
    ║   3. Ejecutar Dijkstra (Caminos más cortos)          ║
    ║   4. Ejecutar Huffman (Compresión de texto)          ║
    ╚══════════════════════════════════════════════════════╝
    """)


def obtener_archivo_grafo() -> str:
    """
    Solicita al usuario la ruta del archivo CSV del grafo.

    Muestra los archivos disponibles en el directorio data/grafos/
    y permite al usuario seleccionar uno o ingresar una ruta personalizada.

    """
    directorio = "data/grafos"
    
    print("\n" + "-" * 40)
    print("ARCHIVOS DE GRAFO DISPONIBLES:")
    print("-" * 40)
    
    archivos = []
    if os.path.exists(directorio):
        archivos = [f for f in os.listdir(directorio) if f.endswith('.csv')]
        for i, archivo in enumerate(archivos, 1):
            print(f"  {i}. {archivo}")
    
    if not archivos:
        print("  (No hay archivos CSV en data/grafos/)")
    
    print("-" * 40)
    print("Ingrese el número del archivo o la ruta completa:")
    
    entrada = input("> ").strip()
    
    # Si es un número, seleccionar de la lista
    if entrada.isdigit():
        indice = int(entrada) - 1
        if 0 <= indice < len(archivos):
            return os.path.join(directorio, archivos[indice])
        else:
            raise ValueError("Número de archivo inválido")
    
    # Si es una ruta, verificar que exista
    if os.path.exists(entrada):
        return entrada
    
    # Intentar en el directorio por defecto
    ruta_default = os.path.join(directorio, entrada)
    if os.path.exists(ruta_default):
        return ruta_default
    
    raise FileNotFoundError(f"No se encontró el archivo: {entrada}")


def obtener_archivo_texto() -> str:
    """
    Solicita al usuario la ruta del archivo TXT para Huffman.
    """
    directorio = "data/textos"
    
    print("\n" + "-" * 40)
    print("ARCHIVOS DE TEXTO DISPONIBLES:")
    print("-" * 40)
    
    archivos = []
    if os.path.exists(directorio):
        archivos = [f for f in os.listdir(directorio) if f.endswith('.txt')]
        for i, archivo in enumerate(archivos, 1):
            print(f"  {i}. {archivo}")
    
    if not archivos:
        print("  (No hay archivos TXT en data/textos/)")
    
    print("-" * 40)
    print("Ingrese el número del archivo o la ruta completa:")
    
    entrada = input("> ").strip()
    
    # Si es un número, seleccionar de la lista
    if entrada.isdigit():
        indice = int(entrada) - 1
        if 0 <= indice < len(archivos):
            return os.path.join(directorio, archivos[indice])
        else:
            raise ValueError("Número de archivo inválido")
    
    # Si es una ruta, verificar que exista
    if os.path.exists(entrada):
        return entrada
    
    # Intentar en el directorio por defecto
    ruta_default = os.path.join(directorio, entrada)
    if os.path.exists(ruta_default):
        return ruta_default
    
    raise FileNotFoundError(f"No se encontró el archivo: {entrada}")


def ejecutar_opcion_prim() -> None:
    """
    Ejecuta el algoritmo de Prim.

    """
    try:
        ruta_csv = obtener_archivo_grafo()
        ejecutar_prim(ruta_csv, "docs/evidencias/prim_mst.png")
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")


def ejecutar_opcion_kruskal() -> None:
    """
    Ejecuta el algoritmo de Kruskal.

    """
    try:
        ruta_csv = obtener_archivo_grafo()
        ejecutar_kruskal(ruta_csv, "docs/evidencias/kruskal_mst.png")
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")


def ejecutar_opcion_dijkstra() -> None:
    """
    Ejecuta el algoritmo de Dijkstra.

    """
    try:
        ruta_csv = obtener_archivo_grafo()
       
        ejecutar_dijkstra(ruta_csv, None, "docs/evidencias/dijkstra_paths.png")
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")


def ejecutar_opcion_huffman() -> None:
    """
    Ejecuta el algoritmo de Huffman.

    Solicita el archivo de texto, ejecuta el algoritmo y genera:
    - huffman_tree.png: Visualización del árbol
    - huffman_freq.png: Gráfica de frecuencias

    """
    try:
        ruta_txt = obtener_archivo_texto()
        ejecutar_huffman(
            ruta_txt,
            "docs/evidencias/huffman_tree.png",
            "docs/evidencias/huffman_freq.png"
        )
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")


def pausar() -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def main() -> None:
    """
    Función principal del programa.

    Implementa el bucle del menú interactivo que permite al usuario
    seleccionar y ejecutar los diferentes algoritmos.

    El programa continúa ejecutándose hasta que el usuario seleccione
    la opción 0 (Salir).
    """
    # Asegurar que existan los directorios necesarios
    os.makedirs("docs/evidencias", exist_ok=True)
    os.makedirs("data/grafos", exist_ok=True)
    os.makedirs("data/textos", exist_ok=True)
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "0":
                print("\nFinalizado")
                break
            
            elif opcion == "1":
                print("\n" + "=" * 60)
                print("Ejecutando algoritmo de PRIM...")
                ejecutar_opcion_prim()
                pausar()
            
            elif opcion == "2":
                print("\n" + "=" * 60)
                print("Ejecutando algoritmo de KRUSKAL...")
                ejecutar_opcion_kruskal()
                pausar()
            
            elif opcion == "3":
                print("\n" + "=" * 60)
                print("Ejecutando algoritmo de DIJKSTRA...")
                ejecutar_opcion_dijkstra()
                pausar()
            
            elif opcion == "4":
                print("\n" + "=" * 60)
                print("Ejecutando algoritmo de HUFFMAN...")
                ejecutar_opcion_huffman()
                pausar()
            
            else:
                print("\nOpción no válida.")
                pausar()
        
        except KeyboardInterrupt:
            print("\n\nFinalizado")
            break
        except Exception as e:
            print(f"\nError: {e}")
            pausar()


if __name__ == "__main__":
    main()
