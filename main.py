import pygame

pygame.init()
size = width, height = 1000, 850
screen = pygame.display.set_mode(size)

button_click = pygame.mixer.Sound('Sounds/9283.mp3')

def menu():
    menu = True

    button = Buttons(100, 50)

    while menu:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button.draw_button(300, 300, 'START')


def title_text(message, x, y, font_color=(0, 0, 0), font_type='Pentagra.ttf', font_size=30):  # Функция шрифтов
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Buttons:  # Класс с кнопками
    def __init__(self, wight, height):
        self.wight = wight
        self.height = height
        self.inactive = (23, 204, 58)
        self.active = (13, 162, 58)

    def draw_button(self, x, y, text, work=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.wight:  # если курсор на кнопке
            if y < mouse[1] < x + self.height:
                pygame.draw.rect(screen, self.active, (x, y, self.wight, self.height))  # Сама кнопка
                if click[0] == 1:  # Если была нажата ЛКМ
                    pygame.mixer.Sound.play(button_click)  # Проигрывание звука нажатия кнопки
                    pygame.time.delay(300)  # Задержка 300мс
                    if work is not None:
                        work()
        else:  # Если курсор не на кнопке
            pygame.draw.rect(screen, self.inactive, (x, y, self.wight, self.height))

        title_text(text, x + 10, y + 10)


if __name__ == '__main__':
    menu()
