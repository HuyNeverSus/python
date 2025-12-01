import pygame
import sys
import time
import random
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("file.mp3")
pygame.mixer.music.play(0)

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Karaoke + Meme Khi + ??")

font = pygame.font.SysFont("Courier New", 60,bold=True)

emoji_font = pygame.font.SysFont("Segoe UI Emoji", 40)


lyrics = [
    "Đang ngóng trông có người đan chặt bàn tay ",
    "Nhưng mà người dường như có những đắn đo nên cũng chẳng hay",
    "Vậy thôi thì nàng ơi chớ lắng lo thế gian chỉ vội biệt ly",
    "Riêng tình ta nồng thắm giữa bao xốn xang chẳng sợ điều chi"
]


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
word_delay = 0.4

meme = pygame.image.load("image2.gif") 
meme = pygame.transform.scale(meme, (300, 300))

questions = []
for _ in range(10):
    x = random.randint(WIDTH - 280, WIDTH - 150)
    y = random.randint(HEIGHT//2 - 180, HEIGHT//2 - 120)
    speed = random.uniform(0.5, 1.2)
    questions.append([x, y, speed])

def render_text_multiline(text, font, color, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return [font.render(line, True, color) for line in lines]

line_delay = 1
for line in lyrics:
    words = line.split()
    displayed = ""

    for word in words:
        displayed += word + " "
        start_time = time.time()

        while time.time() - start_time < word_delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            text_surfaces = render_text_multiline(displayed.strip(), font, WHITE, WIDTH - 400)
            y = HEIGHT // 3
            for ts in text_surfaces:
                rect = ts.get_rect(center=(WIDTH//2 - 150, y))
                screen.blit(ts, rect)
                y += ts.get_height() + 10

            screen.blit(meme, (WIDTH - 320, HEIGHT//2 - 150))


            for q in questions:
                YELLOW = (255, 255, 0)
                q_surface = emoji_font.render("❤️", True, YELLOW)
                screen.blit(q_surface, (q[0], q[1]))
                q[1] -= q[2]
                if q[1] < HEIGHT//2 - 220:
                    q[0] = random.randint(WIDTH - 280, WIDTH - 50)
                    q[1] = HEIGHT//2 - 120
                    q[2] = random.uniform(0.5, 1.2)

            pygame.display.flip()

time.sleep(6.0)
pygame.quit()
sys.exit()
