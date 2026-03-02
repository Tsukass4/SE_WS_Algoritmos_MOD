import pygame
import heapq
import sys

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
TAM_CELDA = 30
COLOR_FONDO = (30, 30, 30)

COLOR_ALMACEN = (0, 255, 0)
COLOR_CLIENTE = (255, 0, 0)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_CAMINO = (0, 255, 255)
COLOR_VISITADO = (100, 100, 255)
COLOR_ACTUAL = (255, 255, 0)
COLOR_FRONTERA = (255, 165, 0)
COLOR_VACIO = (200, 200, 200)

# -----------------------------
# DIBUJAR CIUDAD
# -----------------------------
def dibujar_ciudad(ventana, ciudad, inicio, fin, distancias, actual, frontera):
    ventana.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont("Arial", 14)

    filas = len(ciudad)
    columnas = len(ciudad[0])

    for i in range(filas):
        for j in range(columnas):
            x = j * TAM_CELDA
            y = i * TAM_CELDA
            pos = (i, j)

            if pos == inicio:
                color = COLOR_ALMACEN
            elif pos == fin:
                color = COLOR_CLIENTE
            elif ciudad[i][j] == float("inf"):
                color = COLOR_OBSTACULO
            elif ciudad[i][j] == -1:
                color = COLOR_CAMINO
            elif pos == actual:
                color = COLOR_ACTUAL
            elif pos in frontera:
                color = COLOR_FRONTERA
            elif distancias.get(pos, float("inf")) != float("inf"):
                color = COLOR_VISITADO
            else:
                color = COLOR_VACIO

            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

            # Mostrar distancia acumulada
            if distancias.get(pos, float("inf")) != float("inf") and ciudad[i][j] != -1:
                texto = fuente.render(str(distancias[pos]), True, (0, 0, 0))
                ventana.blit(texto, (x + 4, y + 4))

    pygame.display.update()
    pygame.time.delay(60)


# -----------------------------
# DIJKSTRA APLICADO A LOGÍSTICA
# -----------------------------
def dijkstra_logistica(ventana, ciudad, inicio, fin):
    filas = len(ciudad)
    columnas = len(ciudad[0])

    distancias = {(i, j): float("inf") for i in range(filas) for j in range(columnas)}
    distancias[inicio] = 0

    pq = [(0, inicio)]
    vino_de = {}

    while pq:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dist_actual, pos_actual = heapq.heappop(pq)
        frontera = [nodo for _, nodo in pq]

        if dist_actual > distancias[pos_actual]:
            continue

        dibujar_ciudad(ventana, ciudad, inicio, fin, distancias, pos_actual, frontera)

        if pos_actual == fin:
            print("\n🚚 Ruta óptima encontrada para la entrega.")
            print(f"📦 Costo total del recorrido: {distancias[fin]} unidades")

            paso = fin
            while paso in vino_de:
                if paso != inicio and paso != fin:
                    ciudad[paso[0]][paso[1]] = -1
                paso = vino_de[paso]
                dibujar_ciudad(ventana, ciudad, inicio, fin, distancias, None, [])

            pygame.display.set_caption(
                f"Ruta óptima de entrega - Costo total: {distancias[fin]}"
            )
            return

        f, c = pos_actual

        # Movimientos posibles (4 direcciones)
        for df, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nf, nc = f + df, c + dc

            if 0 <= nf < filas and 0 <= nc < columnas:
                if ciudad[nf][nc] != float("inf"):
                    nueva_dist = dist_actual + 1  # Costo uniforme
                    vecino = (nf, nc)

                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        vino_de[vecino] = pos_actual
                        heapq.heappush(pq, (nueva_dist, vecino))

    print("❌ No se encontró ruta disponible.")


# -----------------------------
# MAIN
# -----------------------------
def main():
    pygame.init()

    ALTO = 12
    ANCHO = 20

    ALMACEN = (1, 1)
    CLIENTE = (9, 15)

    # Calles bloqueadas (simulación de tráfico o construcción)
    OBSTACULOS = (
        [(4, i) for i in range(2, 18) if i not in (6, 12)] +
        [(7, i) for i in range(0, 15)] +
        [(i, 10) for i in range(5, 9)]
    )

    ciudad = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]

    for obs in OBSTACULOS:
        ciudad[obs[0]][obs[1]] = float("inf")

    ventana = pygame.display.set_mode((ANCHO * TAM_CELDA, ALTO * TAM_CELDA))
    pygame.display.set_caption("Sistema Experto: Optimización de Rutas de Entrega")

    print("\n--- SISTEMA DE OPTIMIZACIÓN LOGÍSTICA ---")
    print("Almacén:", ALMACEN)
    print("Cliente:", CLIENTE)
    print("Calculando ruta óptima...\n")

    dijkstra_logistica(ventana, ciudad, ALMACEN, CLIENTE)

    # Mantener ventana abierta
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()