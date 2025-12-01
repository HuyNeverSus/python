import sys
from rich import print
from time import sleep
from rich.console import Console

console = Console()

def lyrics():
    lines = [
        ("\nDon't wanna know", 0.09),#1
        ("Kind of dress you're wearing tonight", 0.05),
        ("If he's holding onto you so tight", 0.05),
        ("The way I did before", 0.07),
        ("I overdosed", 0.2), #5
        ("Should've known your love was a game", 0.05),
        ("Now I can't get you out of my brain", 0.05),
        ("Oh, it's such a shame", 0.07),
        ("That we don't talk anymore", 0.05),
        ("We don't...", 0.04), #10
        ("We don't...", 0.04),
        ("We don't talk anymore", 0.05),
        ("We don't...", 0.04),
        ("We don't...", 0.04),
    ]

    for i, (line, char_delay) in enumerate(lines):
        for char in line:
            print(f"[bold][green]{char}[/bold][/green]", end="")

            sys.stdout.flush()
            sleep(char_delay) 

        print()

lyrics()
