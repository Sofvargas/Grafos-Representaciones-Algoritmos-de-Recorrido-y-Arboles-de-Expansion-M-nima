"""
Investigacion sobre los grafos, recorridos y arboles de expansion minima.
"""
from collections import deque
import heapq

INF = float('inf')

#Grafo base

VERTICES = ["A", "B", "C", "D", "E", "F"]
ARISTAS = [
    ("A", "B", 4), ("A", "C", 2), ("B", "C", 1),
    ("B", "D", 5), ("C", "D", 8), ("C", "E", 10),
    ("D", "E", 2), ("D", "F", 6), ("E", "F", 3),
]

#Representaciones

def construir_lista(vertices, aristas):
    """Lista de adyacencia: dict vertice -> [(vecino, peso), ...]."""
    g = {v: [] for v in vertices}
    for u, v, p in aristas:
        g[u].append((v, p))
        g[v].append((u, p))          # no dirigido
    for v in g:
        g[v].sort()                  # orden alfabetico de vecinos
    return g
 
 
def construir_matriz(vertices, aristas):
    """Matriz de adyacencia ponderada: INF = no hay arista."""
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    m = [[INF] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 0
    for u, v, p in aristas:
        m[idx[u]][idx[v]] = p
        m[idx[v]][idx[u]] = p
    return m, idx
 
#Recorrido por anchura (BFS) - O(n+m) con lista

def bfs(grafo, s):
    visitado = {s}
    dist = {s: 0}
    orden = []
    cola = deque([s])
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v, _ in grafo[u]:
            if v not in visitado:
                visitado.add(v)
                dist[v] = dist[u] + 1
                cola.append(v)
    return orden, dist
 
 
def bfs_matriz(m, vertices, s):
    """BFS sobre matriz de adyacencia -- O(n^2)."""
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    visitado = [False] * n
    visitado[idx[s]] = True
    orden, cola = [], deque([idx[s]])
    while cola:
        u = cola.popleft()
        orden.append(vertices[u])
        for v in range(n):
            if u != v and m[u][v] != INF and not visitado[v]:
                visitado[v] = True
                cola.append(v)
    return orden

#Recorrido por profundidad (DFS) - O(n+m) con lista

def dfs(grafo, s, visitado=None, orden=None):
    if visitado is None:
        visitado, orden = set(), []
    visitado.add(s)
    orden.append(s)
    for v, _ in grafo[s]:
        if v not in visitado:
            dfs(grafo, v, visitado, orden)
    return orden
 
 
def dfs_iterativo(grafo, s):
    visitado, orden, pila = set(), [], [s]
    while pila:
        u = pila.pop()
        if u in visitado:
            continue
        visitado.add(u)
        orden.append(u)
        for v, _ in reversed(grafo[u]):
            if v not in visitado:
                pila.append(v)
    return orden

#Algoritmo de Prim - O(m log n) con monticulo binario

def prim(grafo, s):
    visitado = {s}
    heap = [(p, s, v) for v, p in grafo[s]]
    heapq.heapify(heap)
    mst, total = [], 0
    while heap and len(visitado) < len(grafo):
        p, u, v = heapq.heappop(heap)
        if v in visitado:
            continue                 # arista obsoleta
        visitado.add(v)
        mst.append((u, v, p))
        total += p
        for x, px in grafo[v]:
            if x not in visitado:
                heapq.heappush(heap, (px, v, x))
    return mst, total

#Algoritmo de Kruskal - O(m log m) por el ordenamiento

class UnionFind:
    def __init__(self, elementos):
        self.padre = {x: x for x in elementos}
        self.rango = {x: 0 for x in elementos}
 
    def find(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]  # compresion
            x = self.padre[x]
        return x
 
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False             # formaria un ciclo
        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra
        self.padre[rb] = ra          # union por rango
        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1
        return True
 
 
def kruskal(vertices, aristas):
    uf = UnionFind(vertices)
    mst, total = [], 0
    for u, v, p in sorted(aristas, key=lambda a: a[2]):
        if uf.union(u, v):
            mst.append((u, v, p))
            total += p
            if len(mst) == len(vertices) - 1:
                break
    return mst, total

#Demostracion

if __name__ == "__main__":
    g = construir_lista(VERTICES, ARISTAS)
    m, _ = construir_matriz(VERTICES, ARISTAS)
 
    print("Lista de adyacencia:")
    for v in g:
        print(f"  {v}: {g[v]}")
 
    print("\nMatriz de adyacencia:")
    print("     " + "  ".join(f"{v:>3}" for v in VERTICES))
    for v, fila in zip(VERTICES, m):
        celdas = "  ".join(f"{'inf' if x == INF else x:>3}" for x in fila)
        print(f"  {v}  {celdas}")
 
    orden, dist = bfs(g, "D")
    print("\nBFS desde D (lista): ", orden)
    print("BFS desde D (matriz):", bfs_matriz(m, VERTICES, "D"))
    print("Distancias (aristas):", dist)
    print("DFS recursivo desde D:", dfs(g, "D"))
    print("DFS iterativo desde D:", dfs_iterativo(g, "D"))
 
    mst, total = prim(g, "A")
    print("\nPrim desde A:", mst, "peso total =", total)
    mst, total = kruskal(VERTICES, ARISTAS)
    print("Kruskal:     ", mst, "peso total =", total)