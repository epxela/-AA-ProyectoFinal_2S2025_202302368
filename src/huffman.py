import heapq
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# Clase para los nodos del árbol
class Nodo:
    def __init__(self, simbolo=None, frecuencia=0):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierdo = None
        self.derecho = None
    
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia
    
    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None


# Lee un archivo de texto
def leer_texto(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()


# Cuenta cuántas veces aparece cada letra
def calcular_frecuencias(texto):
    return dict(Counter(texto))


# Construye el árbol de Huffman
def construir_arbol(frecuencias):
    if not frecuencias:
        return None
    
    # Crear nodos para cada letra
    cola = [Nodo(letra, freq) for letra, freq in frecuencias.items()]
    heapq.heapify(cola)
    
    # Caso especial: una sola letra
    if len(cola) == 1:
        nodo = heapq.heappop(cola)
        raiz = Nodo(frecuencia=nodo.frecuencia)
        raiz.izquierdo = nodo
        return raiz
    
    # Juntar nodos hasta que quede uno
    while len(cola) > 1:
        izq = heapq.heappop(cola)
        der = heapq.heappop(cola)
        
        padre = Nodo(frecuencia=izq.frecuencia + der.frecuencia)
        padre.izquierdo = izq
        padre.derecho = der
        
        heapq.heappush(cola, padre)
    
    return cola[0]


# Genera los códigos binarios
def generar_codigos(nodo, codigo="", codigos=None):
    if codigos is None:
        codigos = {}
    
    if nodo is None:
        return codigos
    
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo if codigo else "0"
    
    generar_codigos(nodo.izquierdo, codigo + "0", codigos)
    generar_codigos(nodo.derecho, codigo + "1", codigos)
    
    return codigos


# Dibuja el árbol con texto
def arbol_a_texto(nodo, prefijo="", es_izq=True):
    if nodo is None:
        return ""
    
    conector = "├── " if es_izq else "└── "
    
    if nodo.es_hoja():
        simbolo = repr(nodo.simbolo) if nodo.simbolo in [' ', '\n', '\t'] else nodo.simbolo
        resultado = f"{prefijo}{conector}[{simbolo}] f={nodo.frecuencia}\n"
    else:
        resultado = f"{prefijo}{conector}(f={nodo.frecuencia})\n"
    
    nuevo_prefijo = prefijo + ("│   " if es_izq else "    ")
    
    if nodo.izquierdo:
        resultado += arbol_a_texto(nodo.izquierdo, nuevo_prefijo, True)
    if nodo.derecho:
        resultado += arbol_a_texto(nodo.derecho, nuevo_prefijo, False)
    
    return resultado


# Crea imagen del árbol
def dibujar_arbol(raiz, ruta="docs/evidencias/huffman_tree.png"):
    if raiz is None:
        print("Árbol vacío")
        return
    
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 0.2)
    ax.axis('off')
    
    def contar_hojas(nodo):
        if nodo is None:
            return 0
        if nodo.es_hoja():
            return 1
        return contar_hojas(nodo.izquierdo) + contar_hojas(nodo.derecho)
    
    def dibujar(nodo, x, y, ancho):
        if nodo is None:
            return
        
        if nodo.es_hoja():
            # Hoja = rectángulo verde
            simbolo = repr(nodo.simbolo) if nodo.simbolo in [' ', '\n', '\t'] else nodo.simbolo
            rect = mpatches.FancyBboxPatch((x-0.04, y-0.035), 0.08, 0.07,
                boxstyle="round,pad=0.01", facecolor='lightgreen',
                edgecolor='darkgreen', linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y+0.01, f"'{simbolo}'", ha='center', va='center', fontsize=10, fontweight='bold')
            ax.text(x, y-0.02, f"f={nodo.frecuencia}", ha='center', va='center', fontsize=8)
        else:
            # Nodo interno = círculo azul
            circulo = plt.Circle((x, y), 0.035, color='lightblue', ec='darkblue', linewidth=2)
            ax.add_patch(circulo)
            ax.text(x, y, str(nodo.frecuencia), ha='center', va='center', fontsize=10, fontweight='bold')
        
        if not nodo.es_hoja():
            hojas_izq = contar_hojas(nodo.izquierdo)
            hojas_der = contar_hojas(nodo.derecho)
            total = hojas_izq + hojas_der
            
            if total > 0:
                prop = hojas_izq / total
                x_izq = x - ancho * (1 - prop)
                x_der = x + ancho * prop
            else:
                x_izq = x - ancho / 2
                x_der = x + ancho / 2
            
            y_hijo = y - 0.15
            
            if nodo.izquierdo:
                ax.plot([x, x_izq], [y-0.035, y_hijo+0.035], 'k-', linewidth=1.5)
                ax.text((x+x_izq)/2 - 0.02, (y+y_hijo)/2, '0', fontsize=9, color='blue', fontweight='bold')
                dibujar(nodo.izquierdo, x_izq, y_hijo, ancho/2)
            
            if nodo.derecho:
                ax.plot([x, x_der], [y-0.035, y_hijo+0.035], 'k-', linewidth=1.5)
                ax.text((x+x_der)/2 + 0.02, (y+y_hijo)/2, '1', fontsize=9, color='red', fontweight='bold')
                dibujar(nodo.derecho, x_der, y_hijo, ancho/2)
    
    dibujar(raiz, 0, 0, 0.45)
    plt.title("Árbol de Huffman", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Imagen guardada: {ruta}")


# Crea gráfica de frecuencias
def dibujar_frecuencias(frecuencias, ruta="docs/evidencias/huffman_freq.png"):
    if not frecuencias:
        print("No hay datos")
        return
    
    # Ordenar de mayor a menor
    ordenado = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    
    letras = []
    cantidades = []
    for letra, cant in ordenado[:30]:  # Máximo 30
        if letra == ' ':
            letras.append('espacio')
        elif letra == '\n':
            letras.append('\\n')
        elif letra == '\t':
            letras.append('\\t')
        else:
            letras.append(letra)
        cantidades.append(cant)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    colores = plt.cm.viridis(np.linspace(0.2, 0.8, len(letras)))
    barras = ax.bar(range(len(letras)), cantidades, color=colores, edgecolor='black')
    
    ax.set_xticks(range(len(letras)))
    ax.set_xticklabels(letras, rotation=45, ha='right', fontsize=10)
    ax.set_xlabel('Carácter', fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.set_title('Frecuencia de Caracteres', fontsize=14)
    
    for barra, cant in zip(barras, cantidades):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height(),
                str(cant), ha='center', va='bottom', fontsize=8)
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Imagen guardada: {ruta}")


# Función principal
def ejecutar_huffman(ruta_txt, ruta_arbol="docs/evidencias/huffman_tree.png", 
                     ruta_freq="docs/evidencias/huffman_freq.png"):
    
    print("=" * 60)
    print("ALGORITMO DE HUFFMAN")
    print("=" * 60)
    
    # Leer texto
    print(f"\nLeyendo: {ruta_txt}")
    texto = leer_texto(ruta_txt)
    print(f"Caracteres: {len(texto)}")
    
    # Contar frecuencias
    frecuencias = calcular_frecuencias(texto)
    print(f"Letras únicas: {len(frecuencias)}")
    
    # Mostrar frecuencias
    print("\n" + "-" * 40)
    print("FRECUENCIAS:")
    print("-" * 40)
    for letra, cant in sorted(frecuencias.items(), key=lambda x: x[1], reverse=True):
        simbolo = repr(letra) if letra in [' ', '\n', '\t'] else letra
        print(f"  '{simbolo}': {cant}")
    
    # Construir árbol
    raiz = construir_arbol(frecuencias)
    
    # Generar códigos
    codigos = generar_codigos(raiz)
    
    # Mostrar códigos
    print("\n" + "-" * 50)
    print("CÓDIGOS DE HUFFMAN:")
    print("-" * 50)
    print(f"{'Letra':<12} {'Freq':<8} {'Código':<20} {'Bits'}")
    print("-" * 50)
    
    bits_original = len(texto) * 8
    bits_huffman = 0
    
    for letra, codigo in sorted(codigos.items(), key=lambda x: len(x[1])):
        simbolo = repr(letra) if letra in [' ', '\n', '\t'] else f"'{letra}'"
        freq = frecuencias[letra]
        bits = len(codigo)
        bits_huffman += freq * bits
        print(f"  {simbolo:<10} {freq:<8} {codigo:<20} {bits}")
    
    print("-" * 50)
    
    # Compresión
    compresion = (1 - bits_huffman / bits_original) * 100
    print(f"\nBits original:  {bits_original}")
    print(f"Bits Huffman:   {bits_huffman}")
    print(f"Compresión:     {compresion:.2f}%")
    
    # Árbol en texto
    print("\n" + "-" * 40)
    print("ÁRBOL:")
    print("-" * 40)
    print(arbol_a_texto(raiz))
    
    # Generar imágenes
    print("Generando imágenes...")
    dibujar_arbol(raiz, ruta_arbol)
    dibujar_frecuencias(frecuencias, ruta_freq)
    
    # Ejemplo
    print("\n" + "-" * 40)
    print("EJEMPLO:")
    print("-" * 40)
    muestra = texto[:50] if len(texto) > 50 else texto
    print(f"Original:   \"{muestra}...\"")
    codificado = ''.join(codigos[c] for c in muestra)
    print(f"Codificado: {codificado[:100]}...")
    
    print("\n¡Listo!")
    print("=" * 60)
    
    return frecuencias, codigos, raiz


if __name__ == "__main__":
    ejecutar_huffman("data/textos/texto_ejemplo.txt")


# Alias para compatibilidad con main.py
construir_arbol_huffman = construir_arbol
