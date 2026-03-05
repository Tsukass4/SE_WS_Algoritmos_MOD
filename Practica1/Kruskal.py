import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rutas Turísticas Guadalajara - Kruskal")

# posiciones de los lugares
lugares = {
    "Catedral": (450,300),
    "Teatro": (420,260),
    "Hospicio": (500,320),
    "Zoologico": (620,200),
    "Colomos": (300,200),
    "Andares": (250,150),
    "Tlaquepaque": (550,420),
    "Metropolitano": (150,300)
}

# distancias (km)
edges = [
    ("Catedral","Teatro",0.3),
    ("Catedral","Hospicio",0.9),
    ("Hospicio","Zoologico",7),
    ("Catedral","Colomos",5),
    ("Colomos","Andares",1.5),
    ("Colomos","Metropolitano",4),
    ("Catedral","Tlaquepaque",6),
]

# union find
parent = {}
rank = {}

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x,y):
    rx, ry = find(x), find(y)
    if rx != ry:
        parent[ry] = rx
        return True
    return False

# inicializar
for l in lugares:
    parent[l] = l
    rank[l] = 0

edges.sort(key=lambda x:x[2])

mst = []

for e in edges:
    u,v,w = e
    if union(u,v):
        mst.append(e)

# dibujo
running = True

while running:

    screen.fill((30,30,30))

    # dibujar aristas
    for u,v,w in edges:

        x1,y1 = lugares[u]
        x2,y2 = lugares[v]

        color = (80,80,80)

        if (u,v,w) in mst:
            color = (0,255,255)

        pygame.draw.line(screen,color,(x1,y1),(x2,y2),3)

    # dibujar nodos
    for nombre,(x,y) in lugares.items():

        pygame.draw.circle(screen,(255,255,255),(x,y),8)

        font = pygame.font.SysFont(None,20)
        txt = font.render(nombre,True,(255,255,255))
        screen.blit(txt,(x+10,y))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()