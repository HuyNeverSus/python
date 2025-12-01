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
        pygame.mixer.music.play(0)  
        print("🎶 Nhạc nền đang phát...")
    except Exception as e:
        print("❌ Không thể phát nhạc:", e)
else:
    print(f"❌ Không tìm thấy file nhạc ở: {music_path}")

WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vuon may vua hay v1 ")

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
RAIN_COLOR = (200, 200, 255)

# ======================
# 💧 HIỆU ỨNG MƯA
# ======================
class Raindrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(2, 5)
        self.length = random.randint(8, 15)

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)
            self.speed = random.uniform(2, 5)
            self.length = random.randint(8, 15)

    def draw(self, surface):
        pygame.draw.line(surface, RAIN_COLOR, (self.x, self.y), (self.x, self.y + self.length), 2)

raindrops = [Raindrop() for _ in range(100)]

def draw_scanlines(surface):
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(surface, (50, 50, 50), (0, y), (WIDTH, y))

# ======================
# 🌫️ NHIỄU MÀN HÌNH
# ======================
class NoiseSpot:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(2, 6)
        gray = random.randint(80, 180)
        self.color = (gray, gray, gray)
        self.lifetime = random.uniform(0.1, 0.5)
        self.birth = time.time()

    def draw(self, surface):
        if time.time() - self.birth > self.lifetime:
            self.reset()
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

noises = [NoiseSpot() for _ in range(60)]

# ======================
# 🖼️ HIỂN THỊ LỜI
# ======================
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

def render_frame(displayed):
    frame = pygame.Surface((WIDTH, HEIGHT))
    frame.fill((0, 0, 0))

    for drop in raindrops:
        drop.fall()
        drop.draw(frame)

    lines = wrap_text(displayed.strip(), font, WIDTH)
    y = HEIGHT // 2 - len(lines) * font.get_height() // 2
    for l in lines:
        text_surface = font.render(l, True, WHITE)
        rect = text_surface.get_rect(center=(WIDTH // 2, y))
        frame.blit(text_surface, rect)
        y += font.get_height() + 10

    draw_scanlines(frame)
    for n in noises:
        n.draw(frame)

    screen.blit(frame, (0, 0))
    pygame.display.flip()

# ======================
# 🎶 TÍNH TỐC ĐỘ TỰ ĐỘNG THEO NHẠC
# ======================
total_words = sum(len(line.split()) for line in lyrics)
word_delay = song_duration / total_words * 0.75  # tự căn thời gian cho từng từ
line_delay = 0.9
print(f"Tự tính tốc độ: {word_delay:.2f}s mỗi từ")


start_music_time = time.time()

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
