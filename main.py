import pygame as pg
import time

pg.init()

WIDTH, HEIGHT = 1200, 750

WHITE = (0, 0, 0)
RED = (255, 0, 0)
BG = (25, 26, 27)
COLOR_ACTIVE =  (121, 166, 23)
TEXT = (72, 73, 75)
COLOR_PASSIVE = pg.Color("gray")

FPS = 60

def main():
    clock = pg.time.Clock()
    running = True
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    rect_x = WIDTH//2 - 300
    rect_y = HEIGHT//2 - 50
    rect_w = 600
    rect_h = 75
    input_rect = pg.Rect(rect_x, rect_y, rect_w, rect_h)
    word = "hello"    
    text = ""
    color = WHITE
    index = 0
    word_count = 0

    font = pg.font.SysFont("Roboto", 50, bold=True)
    word_surface = font.render(word, True, TEXT, BG)
    margin_x = (rect_w - word_surface.get_width()) // 2
    margin_y = (rect_h - word_surface.get_height()) // 2
    
    pg.display.update()
    active = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_BACKSPACE :
                    if index > 0:
                        text = text[:-1]
                        index -= 1
                elif index >= len(word):
                    if word == text :
                        word_count += 1
                    index = 0
                    text = ""
                else:
                    char = event.unicode
                    text += char

                    if char == word[index]:
                        color = WHITE
                        index += 1  
                    else: 
                        color = RED
                        index = 0
                        text = ""


            if event.type == pg.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
        
        text_surface = font.render(text, True, color)
        
        screen.fill(BG)
        screen.blit(text_surface,(rect_x + margin_x, rect_y + margin_y))         
        screen.blit(word_surface,(rect_x + margin_x, rect_y + margin_y - 250) )
        print(text)
        print(word_count)
        if active:
            color = COLOR_ACTIVE
        else:
            color = COLOR_PASSIVE
        pg.draw.rect(screen, color, input_rect,  2, 3)
        clock.tick(FPS)
        pg.display.flip() 
        
    pg.quit()


if __name__ == "__main__":
    main()
