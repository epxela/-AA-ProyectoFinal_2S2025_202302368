import csv
import heapq
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch


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
            
            grafo[origen].append((destino, peso))
            grafo[destino].append((origen, peso))
    
    return grafo


# Algoritmo de Dijkstra
def algoritmo_dijkstra(grafo, origen):
    if origen not in grafo:
        print(f"Error: nodo '{origen}' no existe")
        return {}, {}
    
    # Distancias infinitas al inicio
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    
    # Para reconstruir rutas
    anterior = {nodo: None for nodo in grafo}
    
    visitados = set()
    heap = [(0, origen)]
    
    while heap:
        dist_actual, nodo_actual = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        for vecino, peso in grafo[nodo_actual]:
            if vecino not in visitados:
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    anterior[vecino] = nodo_actual
                    heapq.heappush(heap, (nueva_dist, vecino))
    
    return distancias, anterior


# Reconstruye la ruta desde origen hasta destino
def reconstruir_ruta(anterior, destino):
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = anterior[actual]
    return ruta[::-1]


# Crea imagen con los caminos más cortos
def dibujar_caminos(grafo, origen, distancias, anterior, ruta="docs/evidencias/dijkstra_paths.png"):
    G = nx.Graph()
    
    # Agregar aristas
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)
    
    # Aristas de los caminos más cortos
    aristas_camino = set()
    for nodo, pred in anterior.items():
        if pred is not None:
            aristas_camino.add((pred, nodo))
            aristas_camino.add((nodo, pred))
    
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42, k=2)
    
    # Aristas normales (gris)
    normales = [(u, v) for u, v in G.edges() if (u, v) not in aristas_camino and (v, u) not in aristas_camino]
    nx.draw_networkx_edges(G, pos, edgelist=normales, edge_color='lightgray', width=1, style='dashed')
    
    # Aristas de caminos (azul)
    resaltadas = [(u, v) for u, v in G.edges() if (u, v) in aristas_camino or (v, u) in aristas_camino]
    nx.draw_networkx_edges(G, pos, edgelist=resaltadas, edge_color='blue', width=2.5)
    
    # Colores de nodos
    colores = []
    for nodo in G.nodes():
        if nodo == origen:
            colores.append('lightgreen')
        elif distancias[nodo] == float('inf'):
            colores.append('lightcoral')
        else:
            colores.append('lightskyblue')
    
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=900, edgecolors='black', linewidths=2)
    
    # Etiquetas con distancias
    etiquetas = {}
    for nodo in G.nodes():
        if nodo == origen:
            etiquetas[nodo] = f"{nodo}\n(origen)"
        elif distancias[nodo] == float('inf'):
            etiquetas[nodo] = f"{nodo}\n(∞)"
        else:
            etiquetas[nodo] = f"{nodo}\n(d={distancias[nodo]})"
    
    nx.draw_networkx_labels(G, pos, etiquetas, font_size=9, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'), font_size=9)
    
    plt.title(f"Dijkstra - Caminos más cortos\nOrigen: {origen}", fontsize=14)
    plt.axis('off')
    
    # Leyenda
    leyenda = [
        Patch(facecolor='lightgreen', edgecolor='black', label='Origen'),
        Patch(facecolor='lightskyblue', edgecolor='black', label='Alcanzable'),
        Patch(facecolor='lightcoral', edgecolor='black', label='No alcanzable'),
    ]
    plt.legend(handles=leyenda, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Imagen guardada: {ruta}")


# Función principal
def ejecutar_dijkstra(ruta_csv, nodo_origen=None, ruta_salida="docs/evidencias/dijkstra_paths.png"):
    print("=" * 60)
    print("ALGORITMO DE DIJKSTRA - Caminos más cortos")
    print("=" * 60)
    
    print(f"\nLeyendo: {ruta_csv}")
    grafo = leer_grafo(ruta_csv)
    print(f"Nodos: {sorted(grafo.keys())}")
    
    # Pedir origen si no se dio
    if nodo_origen is None:
        nodo_origen = input("\nNodo origen: ").strip().upper()
    
    if nodo_origen not in grafo:
        print(f"Error: '{nodo_origen}' no existe")
        return None, None
    
    print(f"\nEjecutando Dijkstra desde '{nodo_origen}'...")
    distancias, anterior = algoritmo_dijkstra(grafo, nodo_origen)
    
    # Mostrar resultados
    print("\n" + "-" * 50)
    print(f"{'Destino':<10} {'Distancia':<12} {'Ruta'}")
    print("-" * 50)
    
    for nodo in sorted(grafo.keys()):
        if nodo == nodo_origen:
            print(f"{nodo:<10} {0:<12} {nodo} (origen)")
        elif distancias[nodo] == float('inf'):
            print(f"{nodo:<10} {'∞':<12} No alcanzable")
        else:
            ruta = reconstruir_ruta(anterior, nodo)
            print(f"{nodo:<10} {distancias[nodo]:<12} {' → '.join(ruta)}")
    
    print("-" * 50)
    
    print("\nGenerando imagen...")
    dibujar_caminos(grafo, nodo_origen, distancias, anterior, ruta_salida)
    
    print("\n¡Listo!")
    print("=" * 60)
    
    return distancias, anterior


if __name__ == "__main__":
    ejecutar_dijkstra("data/grafos/grafo_ejemplo.csv", "A")
