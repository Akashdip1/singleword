import pygame as pg

pg.init()

class Times:
    def __init__(self, time, position, defaulColor, activeColor) -> None:
        self.font = pg.font.SysFont("Ariel", 32)
        self.text = time
        self.position = position
        self.defaultColor = defaulColor
        self.activeColor = activeColor
        self.active = False
        self.time_limit = 30 # seconds
    
    def draw(self, screen):
        color = self.activeColor if self.active else self.defaultColor
        text_surface = self.font.render(self.text, True, color)
        screen.blit(text_surface, self.position)

    def handleEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos 
            text_rect = self.font.render(self.text, True, self.defaultColor).get_rect(topleft=self.position)
            self.active = text_rect.collidepoint(x, y)
            self.time_limit = int(self.text)

class SingleWord:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1200, 750

        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BG = (25, 26, 27)
        self.NEONGREEN = (121, 166, 23)
        self.GRAY = (127, 127, 127)
        
        self.FPS = 60

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.rect_x = self.WIDTH // 2 - 300
        self.rect_y = self.HEIGHT // 2 - 50
        self.rect_w = 600
        self.rect_h = 75
        self.input_rect = pg.Rect(self.rect_x, self.rect_y, self.rect_w, self.rect_h)
        self.font = pg.font.SysFont("Roboto", 50, bold=True)
        self.time_limit = 30
        self.correct_chars = 0
        self.key_pressed = 0
        self.elapsed_time = 0
        self.accuracy = 0
        self.time_left = 0
        self.wpm = 0
        
        self.shiftpos = 10 
        self.time15_pos = (self.WIDTH//2 - 60 - self.shiftpos, self.rect_y + 200)
        self.time30_pos = (self.WIDTH//2 - 180, self.rect_y + 200)
        self.time60_pos = (self.WIDTH//2 + 60, self.rect_y + 200)
        self.time120_pos = (self.WIDTH//2 + 180 , self.rect_y + 200)

      
    def start_screen(self) -> str:
        running = True
        input_text = ""
        input_index = 0

        time15 = Times("15", self.time15_pos, self.GRAY, self.NEONGREEN)
        time30 = Times("30", self.time30_pos, self.GRAY, self.NEONGREEN)
        time60 = Times("60", self.time60_pos, self.GRAY, self.NEONGREEN)
        time120 = Times("120", self.time120_pos, self.GRAY, self.NEONGREEN)

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
                    elif (
                        event.key == pg.K_RETURN or event.key == pg.K_SPACE
                    ) and input_text:
                        return input_text
                    elif event.key == pg.K_RETURN and not input_text:
                        SingleWord().main()
                    elif event.key == pg.K_SPACE:
                        continue
                    else:
                        char = event.unicode
                        input_text += char
                        
                time15.handleEvent(event)
                time30.handleEvent(event)
                time60.handleEvent(event)
                time120.handleEvent(event)

            if time15.active:
                self.time_limit = 15 
            elif time60.active:
                self.time_limit = 60 
            elif time120.active:
                self.time_limit = 120 
            else:
                self.time_limit = 30

            input_text_surface = self.font.render(input_text, True, self.WHITE)
            input_text_mar_x = (self.rect_w - input_text_surface.get_width()) // 2
            input_text_mar_y = (self.rect_h - input_text_surface.get_height()) // 2

            self.screen.fill(self.BG)
            self.screen.blit(
                input_text_surface,
                (self.rect_x + input_text_mar_x, self.rect_y + input_text_mar_y),
            )
            
            time15.draw(self.screen)
            time30.draw(self.screen)
            time60.draw(self.screen)
            time120.draw(self.screen)
            
            pg.draw.rect(self.screen, self.NEONGREEN, self.input_rect, 2, 3)
            self.clock.tick(self.FPS)
            pg.display.flip()

    def main_screen(self):
        word = self.start_screen()
        text = ""
        color = self.WHITE
        index = 0
        word_surface = self.font.render('"' + word + '"', True, self.NEONGREEN, self.BG)

        margin_x = (self.rect_w - word_surface.get_width()) // 2
        margin_y = (self.rect_h - word_surface.get_height()) // 2
        
        pg.display.update()
        running = True
        start_time = pg.time.get_ticks()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_BACKSPACE:
                        if index > 0:
                            text = text[:-1]
                            index -= 1
                    elif index >= len(word):
                        if word == text:
                            color = self.NEONGREEN
                        index = 0
                        text = ""
                    else:
                        char = event.unicode
                        text += char
                        self.key_pressed += 1

                        if char == word[index]:
                            color = self.WHITE
                            index += 1
                            self.correct_chars += 1
                        else:
                            color = self.RED
                            index = 0
                            text = ""

            if self.elapsed_time >= self.time_limit:
                running = False
            if self.key_pressed > 0:
                self.accuracy = int((self.correct_chars / self.key_pressed) * 100)
            else:
                self.accuracy = 0
            self.wpm = (
                (self.correct_chars / 5) / (self.elapsed_time / 60)
                if self.elapsed_time > 0
                else 0
            )
            self.wpm = round(self.wpm, 1)
            self.elapsed_time = (pg.time.get_ticks() - start_time) / 1000  # seconds

            self.time_left = round((self.time_limit - self.elapsed_time), 2)

            text_surface = self.font.render(text, True, color)
            text_mar_x = (self.rect_w - text_surface.get_width()) // 2
            text_mar_y = (self.rect_h - text_surface.get_height()) // 2

            accuracy_surface = self.font.render(str(self.accuracy), True, self.WHITE)
            accuracy_mar_x = (self.rect_w - accuracy_surface.get_width()) // 2
            accuracy_mar_y = (self.rect_h - accuracy_surface.get_height()) // 2

            time_surface = self.font.render(str(self.time_left), True, self.WHITE)

            self.screen.fill(self.BG)
            self.screen.blit(
                text_surface, (self.rect_x + text_mar_x, self.rect_y + text_mar_y)
            )
            self.screen.blit(
                word_surface, (self.rect_x + margin_x, self.rect_y + margin_y - 250)
            )
            self.screen.blit(
                accuracy_surface,
                (
                    self.rect_x + accuracy_mar_x - 300,
                    self.rect_y + 200 + accuracy_mar_y,
                ),
            )
            self.screen.blit(
                time_surface,
                (
                    self.rect_x + accuracy_mar_x + 300,
                    self.rect_y + accuracy_mar_y + 200,
                ),
            )
            pg.draw.rect(self.screen, color, self.input_rect, 2, 3)
            self.clock.tick(self.FPS)
            pg.display.flip()

    def result_screen(self):
        wpm_surface = self.font.render(str(self.wpm), True, self.WHITE)
        wpm_mar_x = (self.rect_w - wpm_surface.get_width()) // 2
        wpm_mar_y = (self.rect_h - wpm_surface.get_height()) // 2
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
                        SingleWord().main()
            self.screen.fill(self.BG)
            self.screen.blit(
                wpm_surface, (self.rect_x + wpm_mar_x, self.rect_y + wpm_mar_y)
            )
            self.clock.tick(self.FPS)
            pg.display.flip()

    def main(self):
        self.main_screen()
        self.result_screen()
        pg.quit()


SingleWord().main()
