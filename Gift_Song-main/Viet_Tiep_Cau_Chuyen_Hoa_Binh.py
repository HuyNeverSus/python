import sys
from rich import print
from time import sleep
from rich.console import Console

console = Console()

def lyrics():
    lines = [
        ("....",0.01),#1
        ("Tạ ơn những người gìn giữ nước non Đại Việt nghìn năm trước", 0.08),
        ("Tạ ơn người Cha già của chúng ta trên con đường cứu nước\n", 0.08),
        ("Để cho đất nước yên vui từ đó...", 0.07),
        ("Để cho đỏ thắm màu cờ tự do...",0.07),#5
        ("Để những tiếng cười vang khắp nơi từ ngày chiến thắng", 0.09), 
        ("Cùng tôi viết tiếp câu chuyện hoà bình", 0.05), 
        ("Nhìn quê hương sáng tươi trong bình minh", 0.05),
        ("Nhìn ánh nắng chiếu rực rỡ quốc kỳ tung bay phấp phới", 0.08),
        ("Cùng tôi viết tiếp câu chuyện hoà bình", 0.05),#10
        ("Nhìn quê hương sáng tươi trong bình minh",0.05),
        ("Nhìn ánh nắng chiếu rực rỡ quốc kỳ tung bay phấp phới", 0.08),
        ("Nhìn ánh nắng chiếu rực rỡ quốc kỳ tung bay phấp phới", 0.08),
        ("...", 0.05),
    ]

    for i, (line, char_delay) in enumerate(lines):
        for char in line:
            print(f"[bold][blue1]{char}[/bold][/blue1]", end="")
                
            sys.stdout.flush()
            sleep(char_delay) 

        print()

lyrics()
