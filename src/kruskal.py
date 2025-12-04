import csv
import matplotlib.pyplot as plt
import networkx as nx


# Estructura para detectar ciclos
class UnionFind:
    def __init__(self):
        self.padre = {}
        self.rango = {}
    
    def agregar(self, x):
        if x not in self.padre:
            self.padre[x] = x
            self.rango[x] = 0
    
    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]
    
    def unir(self, x, y):
        px, py = self.encontrar(x), self.encontrar(y)
        if px == py:
            return False
        if self.rango[px] < self.rango[py]:
            px, py = py, px
        self.padre[py] = px
        if self.rango[px] == self.rango[py]:
            self.rango[px] += 1
        return True


# Lee el grafo desde un CSV
def leer_grafo(ruta):
    nodos = set()
    aristas = []
    
    with open(ruta, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            origen = fila['origen'].strip()
            destino = fila['destino'].strip()
            peso = int(fila['peso'])
            
            nodos.add(origen)
            nodos.add(destino)
            aristas.append((origen, destino, peso))
    
    return nodos, aristas


# Convierte aristas a grafo de adyacencia
def aristas_a_grafo(aristas):
    grafo = {}
    for origen, destino, peso in aristas:
        if origen not in grafo:
            grafo[origen] = []
        if destino not in grafo:
            grafo[destino] = []
        grafo[origen].append((destino, peso))
        grafo[destino].append((origen, peso))
    return grafo


# Algoritmo de Kruskal
def algoritmo_kruskal(nodos, aristas):
    if not nodos or not aristas:
        return [], 0
    
    # Ordenar aristas por peso
    aristas_ordenadas = sorted(aristas, key=lambda x: x[2])
    
    uf = UnionFind()
    for nodo in nodos:
        uf.agregar(nodo)
    
    mst = []
    peso_total = 0
    
    for origen, destino, peso in aristas_ordenadas:
        # Si no forma ciclo, agregar al MST
        if uf.unir(origen, destino):
            mst.append((origen, destino, peso))
            peso_total += peso
            
         
            if len(mst) == len(nodos) - 1:
                break
    
    return mst, peso_total


# Crea imagen del MST
def dibujar_mst(grafo, mst, ruta="docs/evidencias/kruskal_mst.png"):
    G = nx.Graph()
    
    # Agregar aristas
    agregadas = set()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            arista = tuple(sorted([nodo, vecino]))
            if arista not in agregadas:
                G.add_edge(nodo, vecino, weight=peso)
                agregadas.add(arista)
    
    # Marcar aristas del MST
    aristas_mst = set()
    for origen, destino, peso in mst:
        aristas_mst.add(tuple(sorted([origen, destino])))
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=2)
    
    # Aristas normales
    normales = [(u, v) for u, v in G.edges() if tuple(sorted([u, v])) not in aristas_mst]
    nx.draw_networkx_edges(G, pos, edgelist=normales, edge_color='lightgray', width=1, style='dashed')
    
    # Aristas MST
    resaltadas = [(u, v) for u, v in G.edges() if tuple(sorted([u, v])) in aristas_mst]
    nx.draw_networkx_edges(G, pos, edgelist=resaltadas, edge_color='green', width=3)
    
    # Nodos y etiquetas
    nx.draw_networkx_nodes(G, pos, node_color='lightyellow', node_size=700, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'), font_size=10)
    
    peso_total = sum(p for _, _, p in mst)
    plt.title(f"Kruskal - MST\nPeso total: {peso_total}", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Imagen guardada: {ruta}")


# Función principal
def ejecutar_kruskal(ruta_csv, ruta_salida="docs/evidencias/kruskal_mst.png"):
    print("=" * 60)
    print("ALGORITMO DE KRUSKAL - MST")
    print("=" * 60)
    
    print(f"\nLeyendo: {ruta_csv}")
    nodos, aristas = leer_grafo(ruta_csv)
    print(f"Nodos: {sorted(nodos)}")
    print(f"Aristas: {len(aristas)}")
    
    print("\nEjecutando Kruskal...")
    mst, peso_total = algoritmo_kruskal(nodos, aristas)
    
    print("\n" + "-" * 40)
    print("ARISTAS DEL MST (orden de selección):")
    print("-" * 40)
    for i, (origen, destino, peso) in enumerate(mst, 1):
        print(f"  {i}. {origen} -- {destino} (peso: {peso})")
    print("-" * 40)
    print(f"PESO TOTAL: {peso_total}")
    
    print("\nGenerando imagen...")
    grafo = aristas_a_grafo(aristas)
    dibujar_mst(grafo, mst, ruta_salida)
    
    print("\n¡Listo!")
    print("=" * 60)
    
    return mst, peso_total


if __name__ == "__main__":
    ejecutar_kruskal("data/grafos/grafo_ejemplo.csv")
