import pygame as pg
import time

pg.init()

WIDTH, HEIGHT = 1200, 750

BG = (25, 26, 27)
TEXT = (121, 166, 23)

FPS = 60

def main():
    clock = pg.time.Clock()
    running = True
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG)
    pg.draw.rect(screen, TEXT, pg.Rect(WIDTH//2 - 300, HEIGHT//2 - 50, 600, 75),  2, 3)
    pg.display.update()
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        clock.tick(FPS)
        
    pg.quit()


if __name__ == "__main__":
    main()
