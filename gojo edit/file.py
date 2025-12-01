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
pygame.display.set_caption("dồ ái mồ")
font = pygame.font.SysFont("Courier New", 50, bold=True)
clock = pygame.time.Clock()

# ==== VIDEO SETUP ====
video_path = r"C:\Users\tranv\Downloads\python\gojo edit\file.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Không mở được VIDEO:", video_path)
    sys.exit()

lyrics = [
    ("""Em phone cho mình : bên cạnh em được ko?""", 0, 2.5),
    ("Anh nói với nàng ko là ko !!", 0, 1.9),
    ("đời a ko còn e nên trong tim này", 0, 2.5),
    ("chỉ còn khoảng trống..", 0, 1.5),
    ("Để nàng xa tầm tay", 0, 1.5),
    ("Anh nghĩ là việc làm đúng đắn", 0, 1.9),
    ("đã từng thương thì thôi", 0, 1.5),
    ("anh mong sau này em sẽ đc thương hơn", 0, 2.5),
]

WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# ===================================================
# EFFECT FUNCTIONS (giữ nguyên hết)
# ===================================================
# ==================== HIỆU ỨNG ĐỐM TRẮNG NHẠT NHỎ BAY VÔ ĐỊNH ====================
def generate_dust_particles(n=90):  # 60 là mật độ thấp, rất nhẹ
    particles = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(2.0, 3.5)        # rất nhỏ
        speed_x = random.uniform(-1.8, 1.8)    # di chuyển chậm, vô định
        speed_y = random.uniform(-0.9, 0.9)
        alpha = random.randint(120, 220)         # nhạt, trong suốt
        particles.append([x, y, size, speed_x, speed_y, alpha])
    return particles

def update_and_draw_dust(surface, particles):
    for p in particles:
        # Cập nhật vị trí
        p[0] += p[3]
        p[1] += p[4]
        
        # Reset khi ra khỏi màn hình
        if p[0] < 0 or p[0] > WIDTH:
            p[0] = random.randint(0, WIDTH)
            p[1] = random.randint(0, HEIGHT)
        if p[1] < 0 or p[1] > HEIGHT:
            p[0] = random.randint(0, WIDTH)
            p[1] = random.randint(0, HEIGHT)
        
        # Vẽ đốm tròn nhạt
        dust_surf = pygame.Surface((int(p[2]*4), int(p[2]*4)), pygame.SRCALPHA)
        pygame.draw.circle(dust_surf, (255, 255, 255, int(p[5])), 
                          (int(p[2]*2), int(p[2]*2)), int(p[2]*2))
        surface.blit(dust_surf, (int(p[0] - p[2]*2), int(p[1] - p[2]*2)))

# Khởi tạo danh sách đốm trắng
dust_particles = generate_dust_particles(60)  # 60 đốm → mật độ thấp, rất nhẹ
def draw_scanlines(surface):
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(surface, (15, 15, 15), (0, y), (WIDTH, y))



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





# ===================================================
# TEXT FUNCTIONS
# ===================================================
def wrap_text(text, font, max_width):
    return [text]   # ← BẮT BUỘC TRẢ VỀ 1 DÒNG DUY NHẤT, KHÔNG XUỐNG DÒNG

def draw_song_info(surface):
    overlay = pygame.Surface((330, 90), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 160), (0, 0, 330, 90), border_radius=10)
    pygame.draw.circle(overlay, (255, 255, 255), (40, 45), 25)
    pygame.draw.rect(overlay, (0, 0, 0), (30, 30, 6, 30))
    pygame.draw.rect(overlay, (0, 0, 0), (44, 30, 6, 30))
    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    artist_font = pygame.font.SysFont("Arial", 24)
    overlay.blit(title_font.render("Em Di Di ver1", True, (255, 230, 200)), (80, 18))
    overlay.blit(artist_font.render("Lil Liem", True, (230, 230, 230)), (80, 50))
    surface.blit(overlay, (40, HEIGHT - 110))


    
def draw_lyrics_with_background(lines):
    if not lines:
        return

    # ===== VỊ TRÍ LYRICS (bạn có thể chỉnh ở đây) =====
    base_x = WIDTH // 2
    base_y = HEIGHT - 180        # sát đáy (rất đẹp cho edit)
    # base_y = int(HEIGHT * 0.78)   # hoặc vị trí giữa dưới
    # ===================================================

    # FIX: Tăng khoảng cách giữa dòng lên 30px để background không trùng
    line_height = font.get_height() + 30  # 58 (font height) + 30 = 88px tổng
    total_height = len(lines) * line_height - 30  # trừ bớt để cân đối
    start_y = base_y - total_height // 2

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(base_x, start_y + i * line_height))

        # FIX: Giảm padding_y xuống 15 để background nhỏ gọn hơn, không chạm nhau
        padding_x = 70
        padding_y = 15
        bg_width = text_surface.get_width() + padding_x * 2
        bg_height = text_surface.get_height() + padding_y * 2

        # Tạo background riêng cho TỪNG DÒNG (không chung khối) → không trùng
        bg_surf = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 0, 0, 190), (0, 0, bg_width, bg_height), border_radius=20)
        pygame.draw.rect(bg_surf, (255, 255, 255, 50), (0, 0, bg_width, bg_height), width=3, border_radius=20)

        bg_rect = bg_surf.get_rect(center=text_rect.center)
        screen.blit(bg_surf, bg_rect.topleft)
        screen.blit(text_surface, text_rect)

# ===================================================
# INITIALIZE LAYERS
# ===================================================

scanline_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
draw_scanlines(scanline_layer)
stars = generate_stars()


# ===================================================
# CHỈ SỬA TỪ ĐÂY TRỞ XUỐNG
# ===================================================
running = True
current_line = 0
hold_start = None        # Thêm dòng này (duy nhất thêm 1 biến)

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
    
    update_stars(screen, stars)
    screen.blit(scanline_layer, (0, 0))
    update_and_draw_dust(screen, dust_particles)

    # ---------------- LYRICS (ĐÃ LOẠI BỎ WORD DELAY) ----------------
    if current_line < len(lyrics):
        text, _, hold_time = lyrics[current_line]   # Bỏ qua giá trị delay cũ
        now = time.time()

        # Hiển thị nguyên dòng ngay lập tức
        lines = wrap_text(text, font, WIDTH - 100)
        draw_lyrics_with_background(lines)

        # Bắt đầu đếm thời gian giữ dòng
        if hold_start is None:
            hold_start = now

        # Khi giữ đủ thời gian → chuyển dòng
        if now - hold_start >= hold_time:
            current_line += 1
            hold_start = None

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