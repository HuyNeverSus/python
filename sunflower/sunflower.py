import turtle
import json

def draw_from_json(json_file):
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(800, 800)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    screen.tracer(0)

    # === ĐỌC FILE JSON ===
    with open(json_file) as f:
        regions = json.load(f)

    # === LẤY TẤT CẢ CÁC ĐIỂM ĐỂ TÍNH TỶ LỆ ===
    all_points = [(p[0], p[1]) 
                  for r in regions 
                  for p in r['contour']]

    min_x = min(p[0] for p in all_points)
    max_x = max(p[0] for p in all_points)
    min_y = min(p[1] for p in all_points)
    max_y = max(p[1] for p in all_points)

    width = max_x - min_x
    height = max_y - min_y

    scale = min(600 / width, 600 / height)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    # === VẼ TỪNG VÙNG ===
    for r in regions:
        color = '#{:02x}{:02x}{:02x}'.format(
            int(r['color'][0]),
            int(r['color'][1]),
            int(r['color'][2])
        )
        t.color(color, color)

        points = r['contour']

        t.begin_fill()
        t.penup()

        # Điểm đầu tiên
        x = (points[0][0] - center_x) * scale
        y = (center_y - points[0][1]) * scale
        t.goto(x, y)
        t.pendown()

        # Các điểm tiếp theo
        for point in points[1:]:
            x = (point[0] - center_x) * scale
            y = (center_y - point[1]) * scale
            t.goto(x, y)

        # đóng vùng
        t.goto((points[0][0] - center_x) * scale,
               (center_y - points[0][1]) * scale)
        t.end_fill()

    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    draw_from_json("sunflowers.json")
