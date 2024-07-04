import pygame
import serial
import time
import random

# Arduino bilan serial portni o'rnating
ser = serial.Serial('COM12', 9600)  # Bu yerda COM3 ni Arduino ulangan portga almashtiring
time.sleep(2)  # Serial bog'lanishni o'rnatish uchun kuting

# Pygame-ni boshlash
pygame.init()

# Ovozlarni yuklash
eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over.mp3')

# O'yin ekranini yaratish
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Joystik bilan Snake o'yini")

# Ranglar
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Ilonning boshlang'ich holati
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction

# O'yin tezligi
speed = 15
clock = pygame.time.Clock()

# Oziq-ovqat
food_pos = [random.randrange(1, (600//10)) * 10, random.randrange(1, (600//10)) * 10]
food_spawn = True

# Ballarni saqlash
score = 0

# O'yin tugadi funksiyasi
def game_over():
    game_over_sound.play()  # O'yin tugaganda ovozni ijro etish
    my_font = pygame.font.SysFont('times new roman', 50)
    GO_surf = my_font.render('Game Over', True, red)
    GO_rect = GO_surf.get_rect()
    GO_rect.midtop = (300, 250)
    screen.blit(GO_surf, GO_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Ballarni ko'rsatish funksiyasi
def show_score():
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surf = score_font.render(f'Score: {score}', True, white)
    score_rect = score_surf.get_rect()
    score_rect.midtop = (50, 10)
    screen.blit(score_surf, score_rect)

# O'yin tsikli
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Arduinodan joystik ma'lumotlarini o'qish
    line = ser.readline().decode('utf-8').strip()
    if line:
        parts = line.split(" ")
        x_part = parts[0].split(":")[1]
        y_part = parts[1].split(":")[1]

        x_position = int(x_part)
        y_position = int(y_part)

        # Joystik holatiga qarab ilon yo'nalishini o'zgartirish
        if x_position < 400:
            change_to = 'LEFT'
        if x_position > 600:
            change_to = 'RIGHT'
        if y_position < 400:
            change_to = 'UP'
        if y_position > 600:
            change_to = 'DOWN'

    # Ilonning yo'nalishini o'zgartirish
    if change_to == 'UP' and not snake_direction == 'DOWN':
        snake_direction = 'UP'
    if change_to == 'DOWN' and not snake_direction == 'UP':
        snake_direction = 'DOWN'
    if change_to == 'LEFT' and not snake_direction == 'RIGHT':
        snake_direction = 'LEFT'
    if change_to == 'RIGHT' and not snake_direction == 'LEFT':
        snake_direction = 'RIGHT'

    # Ilonning holatini yangilash
    if snake_direction == 'UP':
        snake_pos[1] -= 10
    if snake_direction == 'DOWN':
        snake_pos[1] += 10
    if snake_direction == 'LEFT':
        snake_pos[0] -= 10
    if snake_direction == 'RIGHT':
        snake_pos[0] += 10

    # Ilonning tanasini yangilash
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
        eat_sound.play()  # Ilon oziq-ovqatni yeganda ovozni ijro etish
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (600//10)) * 10, random.randrange(1, (600//10)) * 10]

    food_spawn = True
    screen.fill(black)

    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # O'yin shartlari
    if snake_pos[0] < 0 or snake_pos[0] > 590 or snake_pos[1] < 0 or snake_pos[1] > 590:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score()
    pygame.display.update()
    clock.tick(speed)
