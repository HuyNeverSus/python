import pygame
import sys
import time
import random
import cv2
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ===== INIT PYGAME =====
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("file.mp3")
pygame.mixer.music.play(0)  # phát 1 lần
font_normal = pygame.font.SysFont("Segoe UI", 76, bold=True)
font_big    = pygame.font.SysFont("Segoe UI", 116, bold=True)

WIDTH, HEIGHT = 1700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lyrics Fade + Effects")
font = pygame.font.SysFont("Times New Roman ", 70, bold=True)
clock = pygame.time.Clock()

# ===== VIDEO SETUP =====
video_path = r"C:\Users\tranv\Downloads\python\hẹn hò nhưng ko yêu\1128.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Không mở được VIDEO:", video_path)
    sys.exit()

# ===== LYRICS =====
lyrics = [
    ("     ", 1),
    ("em ghét", 1),
    ("trái tim em chỉ là một trong con số", 1.5),
    ("anh sắp xếp", 1),
    ("cứ như một trò chơi tình yêu vĩ mô", 2),
    ("đem tất cả", 1.2),
    ("những chân thành đặt lên vòng xoay tâm lý", 1.5),
    ("con tốt", 1.2),
    ("mang tên em mà anh lựa chọn bước đi", 1.8),
    ("hẹn hò nhưng KHÔNG YÊU", 1.5),
    ("chắc em là kẻ MẤT TRÍ",1.5),
    ("hẹn hò nhưng KHÔNG YÊU", 1),
    ("thế YÊU định nghĩa LÀ GÌ?", 1.5),
    ("chạy về người NGÀN BƯỚC", 1.5),
    ("cớ sao người lại TỪ KHƯỚC",1.5),
    ("một bước quay lại về PHÍA EM", 2),
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ===== FADE PARAMETERS =====
FADE_IN_SPEED = 25
FADE_OUT_SPEED = 25

state = "fade_in"
alpha = 0
lyric_index = 0
start_hold = 0

# ===== EFFECTS FUNCTIONS =====

# ==== STARS ====
def generate_stars(n=10):
    stars = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(0.5, 0.5)
        speed = random.uniform(0.5, 0.2)
        stars.append([x, y, size, speed])
    return stars

def update_stars(surface, stars):
    for s in stars:
        s[1] += s[3]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = random.randint(-20, 0)
        pygame.draw.circle(surface, WHITE, (int(s[0]), int(s[1])), int(s[2]))

# ==== DUST PARTICLES ====
def generate_dust_particles(n=60):
    particles = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(0.5, 1.5)
        speed_x = random.uniform(-0.8, 0.8)
        speed_y = random.uniform(-0.9, 0.9)
        alpha = random.randint(120, 220)
        particles.append([x, y, size, speed_x, speed_y, alpha])
    return particles

def update_and_draw_dust(surface, particles):
    for p in particles:
        p[0] += p[3]
        p[1] += p[4]
        if p[0] < 0 or p[0] > WIDTH or p[1] < 0 or p[1] > HEIGHT:
            p[0] = random.randint(0, WIDTH)
            p[1] = random.randint(0, HEIGHT)
        dust_surf = pygame.Surface((int(p[2]*4), int(p[2]*4)), pygame.SRCALPHA)
        pygame.draw.circle(dust_surf, (255, 255, 255, int(p[5])), (int(p[2]*2), int(p[2]*2)), int(p[2]*2))
        surface.blit(dust_surf, (int(p[0]-p[2]*2), int(p[1]-p[2]*2)))

# ==== SCANLINES ====
def draw_scanlines(surface):
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(surface, (15, 15, 15), (0, y), (WIDTH, y))


# ===== INITIALIZE EFFECTS LAYERS =====
stars = generate_stars()
dust_particles = generate_dust_particles()
scanline_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
draw_scanlines(scanline_layer)

# ===== RUNNING LOOP =====
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ===== VIDEO FRAME =====
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    video_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(video_surface, (0, 0))

    # ===== EFFECTS =====
    update_stars(screen, stars)
    screen.blit(scanline_layer, (0, 0))
    update_and_draw_dust(screen, dust_particles)
    

    # ===== LYRICS FADE =====
    # ===== LYRICS FADE – CHỮ IN HOA TO HƠN =====
    if lyric_index < len(lyrics):
        text, duration = lyrics[lyric_index]

        if state == "fade_in":
            alpha += FADE_IN_SPEED
            if alpha >= 255:
                alpha = 255
                state = "hold"
                start_hold = time.time()
        elif state == "hold":
            if time.time() - start_hold >= duration:
                state = "fade_out"
        elif state == "fade_out":
            alpha -= FADE_OUT_SPEED
            if alpha <= 0:
                alpha = 0
                lyric_index += 1
                state = "fade_in"

        # Tạo surface trong suốt để vẽ nhiều chữ với kích thước khác nhau
        lyric_surface = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
        current_x = WIDTH // 2
        base_y = 80  # cách đáy một chút

        base_font_size = 60
        big_font_size = 100    # chữ in hoa sẽ to hơn
        small_offset_y = 30   # chữ thường hơi hạ thấp xuống cho đẹp

        # Font thường và font to
        font_normal = pygame.font.SysFont("Times New Roman", base_font_size, bold=True)
        font_big = pygame.font.SysFont("Times New Roman", big_font_size, bold=True)

        # Tách từng từ để xử lý riêng
        words = text.split()
        total_width = 0
        word_surfaces = []

        for word in words:
            # Kiểm tra từ có chứa chữ in hoa không (hoặc toàn bộ in hoa)
            is_big = word.isupper() or any(c.isupper() for c in word)

            if is_big:
                f = font_big
                color = (255, 255, 150)  # vàng nhạt cho nổi bật (có thể đổi lại WHITE)
            else:
                f = font_normal
                color = WHITE

            surf = f.render(word, True, color)
            surf.set_alpha(alpha)
            word_surfaces.append((surf, is_big))
            total_width += surf.get_width() + 15  # 15 là khoảng cách giữa các từ

        # Bắt đầu vẽ từ giữa màn hình
        x_start = current_x - total_width // 2

        current_x = x_start
        for surf, is_big in word_surfaces:
            y_pos = base_y + (small_offset_y if not is_big else 0)
            rect = surf.get_rect(centerx=current_x + surf.get_width()//2, y=y_pos)
            lyric_surface.blit(surf, rect)
            current_x += surf.get_width() + 15

        # Vẽ lên màn hình chính
        screen.blit(lyric_surface, (0, HEIGHT - 550))  # điều chỉnh HEIGHT - 500 tùy ý

    pygame.display.update()
    clock.tick(60)

    # ===== CHECK MUSIC =====
    if not pygame.mixer.music.get_busy() and lyric_index >= len(lyrics):
        running = False

cap.release()
pygame.quit()
sys.exit()
