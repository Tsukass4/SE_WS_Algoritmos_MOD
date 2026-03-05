import pygame
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rutas Turísticas Guadalajara - Kruskal")

FONT_NOMBRE = pygame.font.SysFont("arial", 22, bold=True)
FONT_DIST = pygame.font.SysFont("arial", 22, bold=True)

COLOR_FONDO = (20,60,20)

COLOR_ARISTA = (160,160,160)
COLOR_ACTUAL = (255,255,0)
COLOR_ACEPTADA = (0,220,255)
COLOR_RECHAZADA = (255,80,80)

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
# UNION FIND
# -----------------------------

parent={}

def find(x):

    if parent[x]!=x:
        parent[x]=find(parent[x])
    return parent[x]


def union(x,y):

    rx,ry=find(x),find(y)

    if rx!=ry:
        parent[ry]=rx
        return True

    return False


# -----------------------------
# DIBUJO
# -----------------------------

def draw(current,accepted,rejected):

    screen.fill(COLOR_FONDO)

    for u,v,w in edges:

        x1,y1=lugares[u]
        x2,y2=lugares[v]

        color=COLOR_ARISTA

        if (u,v,w)==current:
            color=COLOR_ACTUAL

        if (u,v,w) in accepted:
            color=COLOR_ACEPTADA

        if (u,v,w) in rejected:
            color=COLOR_RECHAZADA

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
# KRUSKAL
# -----------------------------

def kruskal():

    for l in lugares:
        parent[l]=l

    sorted_edges=sorted(edges,key=lambda x:x[2])

    accepted=[]
    rejected=[]

    for e in sorted_edges:

        draw(e,accepted,rejected)
        time.sleep(1)

        u,v,w=e

        if union(u,v):
            accepted.append(e)
        else:
            rejected.append(e)

        draw(None,accepted,rejected)
        time.sleep(0.7)


# -----------------------------
# MAIN
# -----------------------------

running=True

kruskal()

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

pygame.quit()