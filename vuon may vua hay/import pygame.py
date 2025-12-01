import pygame
import sys
import time
import random
import os

pygame.init()
pygame.mixer.init()

# 📂 Đường dẫn tới file nhạc (trong cùng thư mục với file .py)
base_path = os.path.dirname(__file__)
music_path = os.path.join(base_path, "snaptik.vn_MhIxH.wav")

song_duration = 56  # thời gian bài hát (giây)

if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()  # chỉ phát 1 lần
        print("🎶 Nhạc nền đang phát...")
    except Exception as e:
        print("❌ Không thể phát nhạc:", e)
else:
    print(f"❌ Không tìm thấy file nhạc ở: {music_path}")

WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vuon may vua hay v2")

font = pygame.font.SysFont("Courier New", 70, bold=True)

lyrics = [
    "Thổn thức em đã bao đêm ngày",
    "Người đến bên có trong đời này",
    "Từng thước phim cứ như sum vầy",
    "Câu chuyện ta vẫn đang trong đấy",
    "Nàng lấy đi trái tim toi rồii",
    "Dạo bước quanh cớ sao bồi hồi",
    "Cảm giác như đã có cơ hội",
    "Đôi lời yêu anh còn chưa nói..",
    "           ...",
    "           ...",
    "           ...",
    "Nếu không phải anh thì em ơi",
    "Đừng cho ai khác đến đây",
    "Một khu vườn hoa riêng chúng ta",
    "Sẽ không có người lạ",
    "Nếu không phải anh thì em ơi",
    "Đừng cho ai khác bước qua",
    "Một rừng yêu thương",
    "Ta đã gieo",
    "Trong những xanh tươi ngày hạ trong vắt!",
    "Có những ngày xanh",
    "Và anh biết có những ngày sau anh",
    "Kế bên hay bên cạnh",
    "Đến đây yêu thương mỏng manh",
    "Em khẽ đến khẽ đến thật mau",
    "Liệu rằng mai đây sẽ có nhau",
    "Trọn vẹn hay không để tính sau",
    "Hãy cứ xem đây như lần đầu"
]

WHITE = (255, 255, 255)
RED = (220, 20, 60)


# ============================================
# ❤️ HIỆU ỨNG TRÁI TIM (lấy từ code v2)
# ============================================
def draw_heart(surface, x, y, size, color):
    top_radius = size // 2
    pygame.draw.circle(surface, color, (x - top_radius, y), top_radius)
    pygame.draw.circle(surface, color, (x + top_radius, y), top_radius)
    points = [
        (x - size, y),
        (x + size, y),
        (x, y + size * 1.5)
    ]
    pygame.draw.polygon(surface, color, points)


# ============================================
# ✂️ WRAP TEXT (giữ nguyên từ code v1)
# ============================================
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        test_line = current + w + " "
        if font.size(test_line)[0] <= max_width - 200:
            current = test_line
        else:
            lines.append(current.strip())
            current = w + " "
    if current:
        lines.append(current.strip())
    return lines


# ============================================
# 🖼️ HIỂN THỊ KHUNG HÌNH (đã thay nền bằng trái tim)
# ============================================
def render_frame(displayed):
    frame = pygame.Surface((WIDTH, HEIGHT))
    frame.fill((0, 0, 0))

    # hiển thị chữ
    lines = wrap_text(displayed.strip(), font, WIDTH)
    y = HEIGHT // 2 - len(lines) * font.get_height() // 2

    for l in lines:
        text_surface = font.render(l, True, WHITE)
        rect = text_surface.get_rect(center=(WIDTH // 2, y))
        frame.blit(text_surface, rect)
        y += font.get_height() + 10

    # ❤️ Trái tim nhấp nháy (hiệu ứng v2)
    blink = int(time.time() * 2) % 2
    if blink:
        draw_heart(frame, WIDTH // 2, HEIGHT - 120, 45, RED)

    screen.blit(frame, (0, 0))
    pygame.display.flip()


# ============================================
# 🎶 TÍNH TỐC ĐỘ TỰ ĐỘNG THEO NHẠC
# ============================================
total_words = sum(len(line.split()) for line in lyrics)
word_delay = song_duration / total_words * 0.75  # tự căn thời gian cho từng từ
line_delay = 0.9
print(f"Tự tính tốc độ: {word_delay:.2f}s mỗi từ")


start_music_time = time.time()

# ============================================
# 📝 HIỂN THỊ LỜI (giữ nguyên của v1)
# ============================================
for line in lyrics:
    words = line.split()
    displayed = ""

    # Hiển thị từng từ
    for word in words:
        displayed += word + " "
        start_time = time.time()

        while time.time() - start_time < word_delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            render_frame(displayed)

    # Dừng giữa các dòng
    delay_start = time.time()
    while time.time() - delay_start < line_delay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        render_frame(displayed)

# Đợi cho đến khi nhạc phát xong
while pygame.mixer.music.get_busy():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    render_frame(displayed)

pygame.quit()
sys.exit()
