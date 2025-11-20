from pathlib import Path
import struct
import zlib

OUTPUT_DIR = Path(__file__).parent / "assets"


def write_png(path, width, height, pixels):
    def chunk(chunk_type, data):
        chunk_head = struct.pack(">I", len(data)) + chunk_type
        crc = zlib.crc32(chunk_head[4:] + data) & 0xFFFFFFFF
        return chunk_head + data + struct.pack(">I", crc)

    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # no filter for this scanline
        start = y * width
        for x in range(width):
            r, g, b, a = pixels[start + x]
            raw_data.extend([r & 0xFF, g & 0xFF, b & 0xFF, a & 0xFF])

    compressed = zlib.compress(bytes(raw_data))
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    idat = chunk(b"IDAT", compressed)
    iend = chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(header + ihdr + idat + iend)


def make_background():
    width, height = 480, 720
    pixels = []
    bubble_centers = [
        (60, 120, 26), (140, 200, 18), (320, 90, 24),
        (420, 260, 32), (240, 340, 20), (80, 420, 22),
        (360, 500, 28), (160, 620, 18), (280, 660, 20),
    ]
    for y in range(height):
        vertical = y / height
        base_blue = int(60 + 110 * vertical)
        base_green = int(90 + 70 * vertical)
        for x in range(width):
            brightness = 10 + int(25 * vertical)
            r = 20 + brightness
            g = base_green
            b = base_blue
            for bx, by, radius in bubble_centers:
                dx = x - bx
                dy = y - by
                dist_sq = dx * dx + dy * dy
                if dist_sq < radius * radius:
                    factor = (radius * radius - dist_sq) / (radius * radius)
                    b = min(255, b + int(80 * factor))
                    g = min(255, g + int(60 * factor))
            pixels.append((r, g, b, 255))
    return pixels, width, height


def make_ground():
    width, height = 520, 140
    pixels = []
    for y in range(height):
        vertical = y / height
        r = int(200 + 25 * vertical)
        g = int(170 + 20 * vertical)
        b = int(120 + 10 * vertical)
        for x in range(width):
            noise = (3 * ((x * 13 + y * 7) % 5))
            pixels.append((min(255, r + noise), min(255, g + noise), min(255, b + noise), 255))
    return pixels, width, height


def make_turtle():
    width, height = 88, 64
    pixels = [(0, 0, 0, 0) for _ in range(width * height)]

    def set_pixel(x, y, color):
        if 0 <= x < width and 0 <= y < height:
            idx = y * width + x
            pixels[idx] = color

    center_x, center_y = width // 2, height // 2
    shell_radius_x, shell_radius_y = 26, 18
    for y in range(height):
        for x in range(width):
            dx = (x - center_x) / shell_radius_x
            dy = (y - center_y) / shell_radius_y
            if dx * dx + dy * dy <= 1.0:
                shading = int(30 * (1 - abs(dy)))
                set_pixel(x, y, (40, 160 + shading, 120 + shading // 2, 255))

    # shell highlight
    for y in range(height):
        for x in range(width):
            dx = (x - center_x - 6) / (shell_radius_x * 0.7)
            dy = (y - center_y - 4) / (shell_radius_y * 0.7)
            if dx * dx + dy * dy <= 1.0:
                set_pixel(x, y, (60, 200, 160, 255))

    # head
    head_center = (center_x + 30, center_y - 4)
    head_radius = 12
    for y in range(height):
        for x in range(width):
            dx = x - head_center[0]
            dy = y - head_center[1]
            if dx * dx + dy * dy <= head_radius * head_radius:
                set_pixel(x, y, (70, 220, 180, 255))

    # eye
    eye = (head_center[0] + 4, head_center[1] - 2)
    for y in range(eye[1] - 1, eye[1] + 2):
        for x in range(eye[0] - 1, eye[0] + 2):
            set_pixel(x, y, (255, 255, 255, 255))
    set_pixel(eye[0], eye[1], (20, 40, 70, 255))

    # flippers
    flipper_color = (50, 200, 160, 255)
    for offset, y_shift in [(-30, 10), (-24, -8)]:
        for y in range(-8, 12):
            for x in range(-6, 12):
                pos_x = center_x + offset + x
                pos_y = center_y + y + y_shift
                dx = x / 12
                dy = y / 10
                if dx * dx + dy * dy < 1.0:
                    set_pixel(pos_x, pos_y, flipper_color)

    # tail
    for i in range(8):
        set_pixel(center_x - shell_radius_x - 6 + i, center_y + i // 2, (35, 160, 120, 255))
        set_pixel(center_x - shell_radius_x - 6 + i, center_y - i // 2, (35, 160, 120, 255))

    return pixels, width, height


def make_plastic():
    width, height = 96, 320
    pixels = [(0, 0, 0, 0) for _ in range(width * height)]

    def set_pixel(x, y, color):
        if 0 <= x < width and 0 <= y < height:
            pixels[y * width + x] = color

    neck_width = width // 4
    body_width = width - 12
    for y in range(height):
        for x in range(width):
            taper = 6 if y < 40 else 0
            left = (width - body_width) // 2 + taper
            right = (width + body_width) // 2 - taper
            if left <= x <= right:
                value = 190 + (y % 5) * 2
                alpha = 200
                set_pixel(x, y, (value, value + 10, value + 25, alpha))

    # label band
    for y in range(120, 180):
        for x in range(width):
            set_pixel(x, y, (90, 160, 210, 230))

    # highlights
    for y in range(0, height, 12):
        for x in range(width // 2 - 10, width // 2 + 6):
            set_pixel(x, y, (230, 240, 250, 220))

    # cap
    for y in range(0, 22):
        for x in range((width - neck_width) // 2, (width + neck_width) // 2):
            set_pixel(x, y, (70, 130, 200, 255))

    return pixels, width, height


def generate_all(output_dir: Path = OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)

    bg_pixels, bg_w, bg_h = make_background()
    write_png(output_dir / "background.png", bg_w, bg_h, bg_pixels)

    ground_pixels, gw, gh = make_ground()
    write_png(output_dir / "ground.png", gw, gh, ground_pixels)

    turtle_pixels, tw, th = make_turtle()
    write_png(output_dir / "turtle.png", tw, th, turtle_pixels)

    plastic_pixels, pw, ph = make_plastic()
    write_png(output_dir / "plastic.png", pw, ph, plastic_pixels)


def main(output_dir: Path | None = None):
    target_dir = output_dir or OUTPUT_DIR
    generate_all(target_dir)
    print(f"Generated assets in '{target_dir}' directory.")


if __name__ == "__main__":
    main()
