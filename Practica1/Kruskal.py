import pygame
import time
import random

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
TAM_CELDA = 30

COLOR_FONDO = (30, 30, 30)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_VACIO = (200, 200, 200)
COLOR_MST = (0, 255, 255)
COLOR_EXAMINANDO = (255, 255, 0)
COLOR_RECHAZADA = (255, 0, 0)
COLOR_TEXTO = (255, 255, 255)

MODO = "MIN"   # "MIN" = árbol mínimo | "MAX" = árbol máximo

# ----------------------------------------
# DIBUJAR TABLERO + INFORMACIÓN
# ----------------------------------------
def dibujar(ventana, tablero, edges_mst, edge_actual, edges_rechazadas, costo_total, fuente):
    ventana.fill(COLOR_FONDO)
    filas = len(tablero)
    columnas = len(tablero[0])

    # dibujar celdas
    for i in range(filas):
        for j in range(columnas):
            x = j * TAM_CELDA
            y = i * TAM_CELDA

            if tablero[i][j] == float("inf"):
                color = COLOR_OBSTACULO
            else:
                color = COLOR_VACIO

            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

    # dibujar MST
    for (u, v, w) in edges_mst:
        dibujar_arista(ventana, u, v, COLOR_MST, w, fuente)

    # arista actual
    if edge_actual:
        u, v, w = edge_actual
        dibujar_arista(ventana, u, v, COLOR_EXAMINANDO, w, fuente)

    # rechazadas
    for (u, v, w) in edges_rechazadas:
        dibujar_arista(ventana, u, v, COLOR_RECHAZADA, w, fuente)

    # texto informativo
    texto_modo = fuente.render(f"Modo: {MODO}", True, COLOR_TEXTO)
    texto_costo = fuente.render(f"Costo total: {costo_total}", True, COLOR_TEXTO)

    ventana.blit(texto_modo, (10, 10))
    ventana.blit(texto_costo, (10, 30))

    pygame.display.update()
    pygame.time.delay(100)


def dibujar_arista(ventana, u, v, color, peso, fuente):
    (r1, c1) = u
    (r2, c2) = v

    x1 = c1 * TAM_CELDA + TAM_CELDA // 2
    y1 = r1 * TAM_CELDA + TAM_CELDA // 2
    x2 = c2 * TAM_CELDA + TAM_CELDA // 2
    y2 = r2 * TAM_CELDA + TAM_CELDA // 2

    pygame.draw.line(ventana, color, (x1, y1), (x2, y2), 4)

    # dibujar peso en el centro
    xm = (x1 + x2) // 2
    ym = (y1 + y2) // 2
    texto = fuente.render(str(peso), True, (255, 255, 255))
    ventana.blit(texto, (xm - 8, ym - 8))


# ----------------------------------------
# UNION–FIND
# ----------------------------------------
def find(padre, x):
    if padre[x] != x:
        padre[x] = find(padre, padre[x])
    return padre[x]


def union(padre, rango, x, y):
    rx = find(padre, x)
    ry = find(padre, y)

    if rx != ry:
        if rango[rx] < rango[ry]:
            padre[rx] = ry
        elif rango[rx] > rango[ry]:
            padre[ry] = rx
        else:
            padre[ry] = rx
            rango[rx] += 1
        return True
    return False


# ----------------------------------------
# GENERAR ARISTAS
# ----------------------------------------
def generar_aristas(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    edges = []

    for r in range(filas):
        for c in range(columnas):
            if tablero[r][c] == float("inf"):
                continue

            if c + 1 < columnas and tablero[r][c+1] != float("inf"):
                peso = random.randint(1, 20)
                edges.append(((r, c), (r, c+1), peso))

            if r + 1 < filas and tablero[r+1][c] != float("inf"):
                peso = random.randint(1, 20)
                edges.append(((r, c), (r+1, c), peso))

    return edges


# ----------------------------------------
# KRUSKAL VISUAL
# ----------------------------------------
def kruskal_pygame(ventana, tablero, fuente):
    filas = len(tablero)
    columnas = len(tablero[0])

    vertices = [(i, j) for i in range(filas)
                for j in range(columnas)
                if tablero[i][j] != float("inf")]

    aristas = generar_aristas(tablero)

    if MODO == "MIN":
        aristas.sort(key=lambda e: e[2])
    else:
        aristas.sort(key=lambda e: -e[2])

    padre = {v: v for v in vertices}
    rango = {v: 0 for v in vertices}

    edges_mst = []
    edges_rechazadas = []
    costo_total = 0

    for edge in aristas:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        u, v, w = edge

        dibujar(ventana, tablero, edges_mst, edge,
                edges_rechazadas, costo_total, fuente)

        if union(padre, rango, u, v):
            edges_mst.append(edge)
            costo_total += w
        else:
            edges_rechazadas.append(edge)

        dibujar(ventana, tablero, edges_mst, None,
                edges_rechazadas, costo_total, fuente)

    print("Kruskal finalizado")
    print("Costo total:", costo_total)
    return edges_mst


# ----------------------------------------
# MAIN
# ----------------------------------------
def main():
    pygame.init()

    ALTO = 10
    ANCHO = 20

    tablero = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]

    ventana = pygame.display.set_mode(
        (ANCHO * TAM_CELDA, ALTO * TAM_CELDA))
    pygame.display.set_caption(
        f"Kruskal Visual - Red Eléctrica ({MODO})")

    fuente = pygame.font.SysFont("Arial", 16)

    kruskal_pygame(ventana, tablero, fuente)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()