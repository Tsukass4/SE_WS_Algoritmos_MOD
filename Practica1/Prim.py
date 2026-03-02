import pygame
import heapq
import random

# -----------------------------
# CONFIGURACIONES GENERALES
# -----------------------------
TAM_CELDA = 30
COLOR_FONDO = (30, 30, 30)

COLOR_INICIO = (0, 255, 0)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_MST = (0, 255, 255)
COLOR_FRONTERA = (255, 255, 0)
COLOR_VISITADO = (100, 100, 255)
COLOR_VACIO = (200, 200, 200)
COLOR_ARISTA_ACTUAL = (255, 0, 0)
COLOR_TEXTO = (255, 255, 255)

PESO_MIN = 1
PESO_MAX = 20

# -----------------------------
# AUXILIAR
# -----------------------------
def edge_key(u, v):
    return (u, v) if u <= v else (v, u)

# -----------------------------
# DIBUJAR ARISTA
# -----------------------------
def dibujar_arista(ventana, u, v, peso, color, fuente):
    (r1, c1) = u
    (r2, c2) = v

    x1 = c1 * TAM_CELDA + TAM_CELDA // 2
    y1 = r1 * TAM_CELDA + TAM_CELDA // 2
    x2 = c2 * TAM_CELDA + TAM_CELDA // 2
    y2 = r2 * TAM_CELDA + TAM_CELDA // 2

    pygame.draw.line(ventana, color, (x1, y1), (x2, y2), 4)

    xm = (x1 + x2) // 2
    ym = (y1 + y2) // 2
    texto = fuente.render(str(peso), True, (255, 255, 255))
    ventana.blit(texto, (xm - 8, ym - 8))

# -----------------------------
# DIBUJAR TABLERO COMPLETO
# -----------------------------
def dibujar_tablero(ventana, tablero, inicio, en_mst,
                    frontera, visitados, mst_edges,
                    arista_actual, edge_weights,
                    total_cost, fuente):

    ventana.fill(COLOR_FONDO)

    filas = len(tablero)
    columnas = len(tablero[0])

    # Dibujar celdas
    for i in range(filas):
        for j in range(columnas):
            x = j * TAM_CELDA
            y = i * TAM_CELDA

            if (i, j) == inicio:
                color = COLOR_INICIO
            elif tablero[i][j] == float("inf"):
                color = COLOR_OBSTACULO
            elif (i, j) in en_mst:
                color = COLOR_MST
            elif (i, j) in frontera:
                color = COLOR_FRONTERA
            elif (i, j) in visitados:
                color = COLOR_VISITADO
            else:
                color = COLOR_VACIO

            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

    # Dibujar aristas del MST
    for (u, v) in mst_edges:
        peso = edge_weights[edge_key(u, v)]
        dibujar_arista(ventana, u, v, peso, COLOR_MST, fuente)

    # Dibujar arista actual
    if arista_actual:
        u, v = arista_actual
        peso = edge_weights[edge_key(u, v)]
        dibujar_arista(ventana, u, v, peso, COLOR_ARISTA_ACTUAL, fuente)

    # Mostrar texto
    texto_costo = fuente.render(f"Costo total: {total_cost}", True, COLOR_TEXTO)
    ventana.blit(texto_costo, (10, 10))

    pygame.display.update()
    pygame.time.delay(100)

# -----------------------------
# PRIM VISUAL
# -----------------------------
def prim_pygame(ventana, tablero, inicio, edge_weights, fuente):

    filas = len(tablero)
    columnas = len(tablero[0])

    en_mst = set()
    frontera = set()
    visitados = set()
    parent = {}
    min_key = {}
    mst_edges = []
    total_cost = 0

    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] != float("inf"):
                min_key[(i, j)] = float("inf")

    min_key[inicio] = 0
    pq = [(0, inicio)]

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key, nodo = heapq.heappop(pq)

        if nodo in en_mst:
            continue

        en_mst.add(nodo)
        visitados.add(nodo)

        arista_actual = None

        if nodo in parent:
            mst_edges.append((nodo, parent[nodo]))
            total_cost += edge_weights[edge_key(nodo, parent[nodo])]
            arista_actual = (nodo, parent[nodo])

        f, c = nodo
        for df, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nf, nc = f + df, c + dc
            vecino = (nf, nc)

            if (
                0 <= nf < filas and 0 <= nc < columnas and
                tablero[nf][nc] != float("inf") and
                vecino not in en_mst
            ):
                w = edge_weights[edge_key(nodo, vecino)]
                if w < min_key[vecino]:
                    min_key[vecino] = w
                    parent[vecino] = nodo
                    frontera.add(vecino)
                    heapq.heappush(pq, (w, vecino))

        dibujar_tablero(ventana, tablero, inicio,
                        en_mst, frontera, visitados,
                        mst_edges, arista_actual,
                        edge_weights, total_cost,
                        fuente)

    print("Prim finalizado.")
    print("Costo total:", total_cost)

# -----------------------------
# GENERAR PESOS
# -----------------------------
def generar_edge_weights(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    edge_weights = {}

    for r in range(filas):
        for c in range(columnas):
            if tablero[r][c] == float("inf"):
                continue

            u = (r, c)

            if c + 1 < columnas and tablero[r][c+1] != float("inf"):
                v = (r, c+1)
                edge_weights[edge_key(u, v)] = random.randint(PESO_MIN, PESO_MAX)

            if r + 1 < filas and tablero[r+1][c] != float("inf"):
                v = (r+1, c)
                edge_weights[edge_key(u, v)] = random.randint(PESO_MIN, PESO_MAX)

    return edge_weights

# -----------------------------
# MAIN
# -----------------------------
def main():
    pygame.init()

    ALTO = 10
    ANCHO = 20
    INICIO = (5, 12)

    tablero = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]

    ventana = pygame.display.set_mode((ANCHO * TAM_CELDA, ALTO * TAM_CELDA))
    pygame.display.set_caption("Prim Visual - Red Eléctrica")

    fuente = pygame.font.SysFont("Arial", 16)

    edge_weights = generar_edge_weights(tablero)

    prim_pygame(ventana, tablero, INICIO, edge_weights, fuente)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()