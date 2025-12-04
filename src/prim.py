import csv
import heapq
import matplotlib.pyplot as plt
import networkx as nx


# Lee el grafo desde un CSV
def leer_grafo(ruta):
    grafo = {}
    with open(ruta, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            origen = fila['origen'].strip()
            destino = fila['destino'].strip()
            peso = int(fila['peso'])
            
            if origen not in grafo:
                grafo[origen] = []
            if destino not in grafo:
                grafo[destino] = []
            
            # Grafo no dirigido
            grafo[origen].append((destino, peso))
            grafo[destino].append((origen, peso))
    
    return grafo


# Algoritmo de Prim
def algoritmo_prim(grafo, inicio=None):
    if not grafo:
        return [], 0
    
    if inicio is None:
        inicio = next(iter(grafo))
    
    visitados = set()
    mst = []
    peso_total = 0
    
    # Cola:
    heap = [(0, inicio, inicio)]
    
    while heap and len(visitados) < len(grafo):
        peso, origen, actual = heapq.heappop(heap)
        
        if actual in visitados:
            continue
        
        visitados.add(actual)
        
        if origen != actual:
            mst.append((origen, actual, peso))
            peso_total += peso
        
        for vecino, peso_arista in grafo[actual]:
            if vecino not in visitados:
                heapq.heappush(heap, (peso_arista, actual, vecino))
    
    return mst, peso_total


# Crea imagen del MST
def dibujar_mst(grafo, mst, ruta="docs/evidencias/prim_mst.png"):
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
    nx.draw_networkx_edges(G, pos, edgelist=resaltadas, edge_color='red', width=3)
    
    # Nodos y etiquetas
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'), font_size=10)
    
    peso_total = sum(p for _, _, p in mst)
    plt.title(f"Prim - MST\nPeso total: {peso_total}", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Imagen guardada: {ruta}")


# Función principal
def ejecutar_prim(ruta_csv, ruta_salida="docs/evidencias/prim_mst.png"):
    print("=" * 60)
    print("ALGORITMO DE PRIM - MST")
    print("=" * 60)
    
    print(f"\nLeyendo: {ruta_csv}")
    grafo = leer_grafo(ruta_csv)
    print(f"Nodos: {sorted(grafo.keys())}")
    
    print("\nEjecutando Prim...")
    mst, peso_total = algoritmo_prim(grafo)
    
    print("\n" + "-" * 40)
    print("ARISTAS DEL MST:")
    print("-" * 40)
    for i, (origen, destino, peso) in enumerate(mst, 1):
        print(f"  {i}. {origen} -- {destino} (peso: {peso})")
    print("-" * 40)
    print(f"PESO TOTAL: {peso_total}")
    
    print("\nGenerando imagen...")
    dibujar_mst(grafo, mst, ruta_salida)
    
    print("\n¡Listo!")
    print("=" * 60)
    
    return mst, peso_total


if __name__ == "__main__":
    ejecutar_prim("data/grafos/grafo_ejemplo.csv")
