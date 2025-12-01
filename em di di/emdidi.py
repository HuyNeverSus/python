import pygame
import sys
import time
import random
import math
import cv2
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()
pygame.mixer.music.load("file.mp3")
pygame.mixer.music.play(0)

WIDTH, HEIGHT = 1700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("em di di😊")
font = pygame.font.SysFont("Courier New", 58, bold=True)
clock = pygame.time.Clock()

# ==== VIDEO SETUP ====
video_path = r"C:\Users\tranv\Downloads\python\em di di\file.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Không mở được VIDEO:", video_path)
    sys.exit()

lyrics = [
    (" ", 80, 2.2),
    ("Em như ánh sao đang bay trên cao ", 20, 0.6),
    ("Anh chỉ thấy em ở trong chiêm bao", 20, 0.6),
    ("không thể nhớ em vì tim đang đau", 20, 0.6),
    ("Yêu mãi luôn là trong bao lâu?", 20, 0.6),
    ("Anh bị sợ với những lời hứa", 20, 0.8),
    ("Hai ta xa từ ngày mưa ...", 20, 0.8),
    ("Em có nhớ về ngày xưa ...", 20, 0.9),
    ("anh nghĩ là chẳng còn nữa", 20, 1.5),
]

WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# ===================================================
# EFFECT FUNCTIONS (giữ nguyên hết)
# ===================================================
def draw_scanlines(surface):
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(surface, (15, 15, 15), (0, y), (WIDTH, y))

def generate_static_surface():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(80)
    return surf

def update_static_surface(surf):
    arr = pygame.surfarray.pixels3d(surf)
    arr[:] = (random.randint(0, 60),) * 3
    for _ in range(3500):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        bright = random.randint(180, 255)
        arr[x, y] = (bright, bright, bright)
    del arr

def generate_stars(n=40):
    stars = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(1.5, 2.5)
        speed = random.uniform(0.5, 1.2)
        stars.append([x, y, size, speed])
    return stars

def update_stars(surface, stars):
    for s in stars:
        s[1] += s[3]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = random.randint(-20, 0)
        pygame.draw.circle(surface, (255, 255, 255), (int(s[0]), int(s[1])), int(s[2]))

def generate_rain(n=80):
    rain = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        length = random.randint(8, 15)
        speed = random.uniform(3, 7)
        rain.append([x, y, length, speed])
    return rain

def update_rain(surface, rain):
    for drop in rain:
        x, y, length, speed = drop
        pygame.draw.line(surface, (255, 255, 255), (x, y), (x, y + length), 1)
        drop[1] += speed
        if drop[1] > HEIGHT:
            drop[0] = random.randint(0, WIDTH)
            drop[1] = random.randint(-20, 0)

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        test_line = current + w + " "
        if font.size(test_line)[0] <= max_width - 300:
            current = test_line
        else:
            lines.append(current.strip())
            current = w + " "
    if current:
        lines.append(current.strip())
    return lines

def draw_song_info(surface):
    overlay = pygame.Surface((330, 90), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 160), (0, 0, 330, 90), border_radius=10)
    pygame.draw.circle(overlay, (255, 255, 255), (40, 45), 25)
    pygame.draw.rect(overlay, (0, 0, 0), (30, 30, 6, 30))
    pygame.draw.rect(overlay, (0, 0, 0), (44, 30, 6, 30))
    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    artist_font = pygame.font.SysFont("Arial", 24)
    overlay.blit(title_font.render("Em Di Di", True, (255, 230, 200)), (80, 18))
    overlay.blit(artist_font.render("Lil Liem", True, (230, 230, 230)), (80, 50))
    surface.blit(overlay, (40, HEIGHT - 110))

# ===================================================
# INITIALIZE LAYERS
# ===================================================
static_layer = generate_static_surface()
scanline_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
draw_scanlines(scanline_layer)
stars = generate_stars()
rain = generate_rain()

# ===================================================
# HÀM VẼ LYRICS – ĐÃ XÓA VIỀN XANH + KHÔNG HIỆN HỘP TRỐNG
# ===================================================
def draw_lyrics_with_background(lines):
    if not lines or not lines[0].strip():   # ← không vẽ gì nếu chưa có chữ
        return

    total_height = len(lines) * font.get_height() + (len(lines)-1)*10
    start_y = HEIGHT // 2 - total_height // 2

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH//2, start_y + i*(font.get_height()+10)))

        padding_x = 60
        padding_y = 20
        bg_width = text_surface.get_width() + padding_x*2
        bg_height = text_surface.get_height() + padding_y*2

        bg_surf = pygame.Surface((bg_width, bg_height))
        bg_surf.fill((0, 0, 0, ))                             
        pygame.draw.rect(bg_surf, (0, 0, 0, 180), bg_surf.get_rect(), border_radius=16)

        # ĐÃ XÓA HOÀN TOÀN VIỀN XANH Ở ĐÂY
        # pygame.draw.rect(bg_surf, (100, 180, 255, 80), bg_surf.get_rect(), width=3, border_radius=16)

        bg_rect = bg_surf.get_rect(center=text_rect.center)
        screen.blit(bg_surf, bg_rect.topleft)
        screen.blit(text_surface, text_rect)

# ===================================================
# MAIN LOOP (không thay đổi gì)
# ===================================================
running = True
current_line = 0
letter_index = 0
last_char_time = time.time()
hold_start = None

while running:
    # ---------------- VIDEO FRAME ----------------
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
    screen.blit(frame_surface, (0, 0))

    # ---------------- EFFECTS ----------------
    update_static_surface(static_layer)
    screen.blit(static_layer, (0, 0))
    update_stars(screen, stars)
    screen.blit(scanline_layer, (0, 0))
    update_rain(screen, rain)

    # ---------------- LYRICS ----------------
    if current_line < len(lyrics):
        text, delay, hold_time = lyrics[current_line]
        now = time.time()

        if letter_index < len(text) and now - last_char_time > delay / 1000.0:
            letter_index += 1
            last_char_time = now

        if letter_index == len(text):
            if hold_start is None:
                hold_start = now
            elif now - hold_start >= hold_time:
                current_line += 1
                letter_index = 0
                hold_start = None

        displayed = text[:letter_index]
        lines = wrap_text(displayed, font, WIDTH - 100)

        draw_lyrics_with_background(lines)

    # ---------------- INFO ----------------
    draw_song_info(screen)

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
pygame.quit()
sys.exit()