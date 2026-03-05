import pygame
import heapq
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rutas Turísticas Guadalajara - Prim")

FONT_NOMBRE = pygame.font.SysFont("arial", 22, bold=True)
FONT_DIST = pygame.font.SysFont("arial", 22, bold=True)

COLOR_FONDO = (20,60,20)

COLOR_ARISTA = (160,160,160)
COLOR_ACTUAL = (255,255,0)
COLOR_ACEPTADA = (0,220,255)

COLOR_NOMBRE = (255,255,200)
COLOR_DIST = (240,240,240)

START_NODE = "Teatro"

# -----------------------------
# POSICIONES
# -----------------------------

lugares = {

"Teatro":(600,380),
"Hospicio":(700,450),

"Zoologico":(980,160),

"Colomos":(380,160),
"Andares":(260,90),

"Metropolitano":(160,380),

"Estadio":(820,250),

"PlazaSol":(380,650),

"Tlaquepaque":(900,650)

}

# -----------------------------
# CONEXIONES
# -----------------------------

edges=[

("Teatro","Hospicio",0.7),

("Teatro","PlazaSol",7),
("Teatro","Metropolitano",8),

("Hospicio","Zoologico",7),
("Hospicio","Estadio",4),

("Colomos","Andares",1.5),
("Colomos","Metropolitano",4),
("Colomos","Estadio",3),

("Andares","Metropolitano",6),

("Estadio","Zoologico",4),

("Metropolitano","PlazaSol",3),

("PlazaSol","Tlaquepaque",7)

]

# -----------------------------
# CONSTRUIR GRAFO
# -----------------------------

graph = {}

for u,v,w in edges:

    graph.setdefault(u,[]).append((v,w))
    graph.setdefault(v,[]).append((u,w))

# -----------------------------
# DIBUJO
# -----------------------------

def draw(current_edge, mst_edges):

    screen.fill(COLOR_FONDO)

    for u,v,w in edges:

        x1,y1=lugares[u]
        x2,y2=lugares[v]

        color=COLOR_ARISTA

        if current_edge and (u,v,w)==current_edge:
            color=COLOR_ACTUAL

        if (u,v,w) in mst_edges or (v,u,w) in mst_edges:
            color=COLOR_ACEPTADA

        pygame.draw.line(screen,color,(x1,y1),(x2,y2),4)

        mx=(x1+x2)//2
        my=(y1+y2)//2

        text=FONT_DIST.render(str(w)+" km",True,COLOR_DIST)

        rect=text.get_rect(center=(mx,my))
        pygame.draw.rect(screen,(40,40,40),rect.inflate(6,4))

        screen.blit(text,rect)

    for name,(x,y) in lugares.items():

        pygame.draw.circle(screen,(240,240,240),(x,y),10)

        if name==START_NODE:

            pygame.draw.circle(screen,(255,60,60),(x,y),22,3)

            label=FONT_NOMBRE.render(name+" (Inicio)",True,(255,220,120))

        else:
            label=FONT_NOMBRE.render(name,True,COLOR_NOMBRE)

        screen.blit(label,(x+12,y-12))

    pygame.display.update()

# -----------------------------
# ALGORITMO PRIM
# -----------------------------

def prim():

    visited=set([START_NODE])

    pq=[]

    for v,w in graph[START_NODE]:
        heapq.heappush(pq,(w,START_NODE,v))

    mst_edges=[]

    while pq:

        w,u,v=heapq.heappop(pq)

        draw((u,v,w),mst_edges)
        time.sleep(1)

        if v in visited:
            continue

        visited.add(v)

        mst_edges.append((u,v,w))

        draw(None,mst_edges)
        time.sleep(0.7)

        for to,weight in graph[v]:

            if to not in visited:
                heapq.heappush(pq,(weight,v,to))

# -----------------------------
# MAIN
# -----------------------------

running=True

prim()

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

pygame.quit()