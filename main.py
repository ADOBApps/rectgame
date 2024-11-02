import pygame
import random

import tkinter as tk
from tkinter import messagebox


# Función que llamaremos al perder el juego
def game_over():
    # Creamos una ventana de tkinter
    root = tk.Tk()

    # Ocultamos la ventana padre
    root.withdraw()

    # logramos que dicha ventana y sus widgets se superponga sobre el juego
    root.lift()

    # Creamos una caja de alerta tipo si o no
    answer = messagebox.askyesno(
        title=" Juego finalizado",
        message="¿Desea reiniciar el juego?"
    )

    # Destruimos la ventana
    root.destroy()

    # Devolvemos la decision del usuario
    return answer


# Una función para obtener el código RGB de colores comunes
def obtener_color_rgb(nombre_color):
    colores = {
        'rojo': (255, 0, 0),
        'verde': (0, 255, 0),
        'azul': (0, 0, 255),
        'amarillo': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'blanco': (255, 255, 255),
        'negro': (0, 0, 0),
        'gris': (128, 128, 128),
        'naranja': (255, 165, 0),
        'violeta': (238, 130, 238),
        'marrón': (165, 42, 42),
        'turquesa': (64, 224, 208),
    }

    rgb = colores.get(nombre_color.lower(), None)
    if rgb:
        return rgb
    else:
        return (0, 0, 0)


# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa los rectangulos")

# Colores
WHITE = obtener_color_rgb("blanco")
RED = obtener_color_rgb("rojo")
BLUE = obtener_color_rgb("azul")
GREEN = obtener_color_rgb("verde")

# Variables del juego

# ==> Recipiente
basket_width = 100
basket_height = 20
basket_x = (WIDTH - basket_width) // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 10

# ==> Enemigos
enemy_size = 30
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = 0
enemy_speed = 5

# ==> Objectivos
rect_size = 30
rect_x = random.randint(0, WIDTH - rect_size)
rect_y = 0
rect_speed = 5

score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del recipiente
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # Movimiento del enemigo
    enemy_y += enemy_speed

    # Movimiento del objetivo
    rect_y += rect_speed

    # Movimiento del enemigo
    enemy_y += enemy_speed

    # Comprobar colisiones del objetivo
    if (basket_y < rect_y + rect_size and 
        basket_y + basket_height > rect_y and 
        basket_x < rect_x + rect_size and 
        basket_x + basket_width > rect_x):
        score += 1
        rect_x = random.randint(0, WIDTH - rect_size)
        rect_y = 0

    # Comprobar colisiones del enemigo
    if (basket_y < enemy_y + enemy_size and 
        basket_y + basket_height > enemy_y and 
        basket_x < enemy_x + enemy_size and 
        basket_x + basket_width > enemy_x):
        score -= 1
        enemy_x = random.randint(0, WIDTH - enemy_size)
        enemy_y = 0

    # Reiniciar el enemigo/objetivo si se cae
    if rect_y > HEIGHT:
        rect_x = random.randint(0, WIDTH - rect_size)
        rect_y = 0
    if enemy_y > HEIGHT:
        enemy_x = random.randint(0, WIDTH - enemy_size)
        enemy_y = 0

    # Dibujar en la pantalla
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (basket_x, basket_y, basket_width, basket_height))  # Recipiente
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_size, enemy_size))  # enemigo
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_size, rect_size))  # objetivo

    # Mostrar puntaje
    score_text = font.render(f"Puntaje: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

    if score == -10:
        if game_over() == True:
            # Reiniciamos el puntaje
            score = 0
            score_text = font.render(f"Puntaje: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
        else:
            # Salimos del juego
            pygame.quit()


pygame.quit()
