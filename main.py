import pygame as pg

pg.init()

WIDTH, HEIGHT = 1200, 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG = (25, 26, 27)
COLOR_ACTIVE = NEONGREEN = (121, 166, 23)
COLOR_PASSIVE = pg.Color("gray")

FPS = 60

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
rect_x = WIDTH//2 - 300
rect_y = HEIGHT//2 - 50
rect_w = 600
rect_h = 75
input_rect = pg.Rect(rect_x, rect_y, rect_w, rect_h)
font = pg.font.SysFont("Roboto", 50, bold=True)

correct_chars = 0
elapsed_time = 0
wpm = 0

def start_screen() -> str: 
    running = True 
    input_text = ""
    input_index = 0
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]
                    input_index -= 1
                elif (event.key == pg.K_RETURN or event.key == pg.K_SPACE) and input_text:
                    return input_text
                elif event.key == pg.K_RETURN and not input_text:
                    main_screen()
                elif event.key == pg.K_SPACE:
                    continue
                else:
                    char = event.unicode
                    input_text += char

        input_text_surface = font.render(input_text, True, WHITE)
        input_text_mar_x = (rect_w - input_text_surface.get_width()) // 2 
        input_text_mar_y = (rect_h - input_text_surface.get_height()) // 2
        
        screen.fill(BG)
        screen.blit(input_text_surface,(rect_x + input_text_mar_x, rect_y + input_text_mar_y))         
        pg.draw.rect(screen, NEONGREEN, input_rect,  2, 3)
        clock.tick(FPS)
        pg.display.flip() 

def main_screen():
    word = start_screen() 
    text = ""
    color = WHITE
    index = 0
    word_count = 0
    global correct_chars
    global elapsed_time
    word_surface = font.render('"' + word + '"', True, NEONGREEN, BG)
    
    margin_x = (rect_w - word_surface.get_width()) // 2
    margin_y = (rect_h - word_surface.get_height()) // 2
    
    pg.display.update()
    running = True
    start_time = pg.time.get_ticks()
    time_limit = 30 # seconds
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
                        color = NEONGREEN
                        word_count += 1
                    index = 0
                    text = ""
                else:
                    char = event.unicode
                    text += char

                    if char == word[index]:
                        color = WHITE
                        index += 1  
                        correct_chars += 1
                    else: 
                        color = RED 
                        index = 0
                        text = ""
            elif elapsed_time >=  time_limit:
                running = False
        elapsed_time = (pg.time.get_ticks() - start_time) / 1000 #seconds

        text_surface = font.render(text, True, color)
        text_mar_x = (rect_w - text_surface.get_width()) // 2 
        text_mar_y = (rect_h - text_surface.get_height()) // 2

        screen.fill(BG)
        screen.blit(text_surface,(rect_x + text_mar_x, rect_y + text_mar_y))         
        screen.blit(word_surface,(rect_x + margin_x, rect_y + margin_y - 250) )
        pg.draw.rect(screen, color, input_rect,  2, 3)
        clock.tick(FPS)
        pg.display.flip() 

def result_screen():
    wpm_surface = font.render(str(correct_chars), True, WHITE)
    wpm_mar_x = (rect_w - wpm_surface.get_width()) // 2 
    wpm_mar_y = (rect_h - wpm_surface.get_height()) // 2
    pg.display.update()
    running = True 
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_RETURN:
                    main_screen()
        screen.fill(BG)
        screen.blit(wpm_surface, (rect_x + wpm_mar_x, rect_y + wpm_mar_y))
        clock.tick(FPS)
        pg.display.flip()
def main():
    main_screen()  
    result_screen()
    pg.quit()


if __name__ == "__main__":
    main()
