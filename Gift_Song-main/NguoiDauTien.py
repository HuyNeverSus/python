import sys
from rich import print
from time import sleep
from rich.console import Console

console = Console()

def lyrics():
    lines = [
        ("....",0.02),#1
        ("Hay là em đi theo anh đến nơi", 0.09),
        ("Nơi mà ta không chia đôi quãng đời", 0.09),
        ("Nơi mà có anh cười như năm tháng đôi mươi", 0.09),
        ("Nơi mà bảo giông đều tan...",0.06),#5
        ("Vì có nhau rồi", 0.06), 
        ("Hay để em đi theo anh cho rồi", 0.09), 
        ("Ly biệt tội lắm em đau hết đời", 0.08),
        ("Vắng người đời em...", 0.06),
        ("chỉ còn bóng tối vây quanh", 0.07),#10
        ("Làm ơn đừng bỏ em giữa...",0.08),
        ("Cuộc đời hiu quạnh", 0.07),
    ]

    for i, (line, char_delay) in enumerate(lines):
        for char in line:
            print(f"[bold][blue1]{char}[/bold][/blue1]", end="")
                
            sys.stdout.flush()
            sleep(char_delay) 

        print()

lyrics()
