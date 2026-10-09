#!/usr/bin/env python3
"""Generate the submission architecture diagram without live AWS claims."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1600, 820
BG = "#F7F9FC"
INK = "#18283D"
MUTED = "#53657A"
LINE = "#2C3E55"
BLUE = "#E7F0FB"
GREEN = "#EAF4EC"
GOLD = "#FFF4DF"
ROSE = "#F8E8EE"
VPC = "#EEF2F7"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(name, size)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, size: int, *, bold: bool = False, fill: str = INK) -> None:
    bounds = draw.textbbox((0, 0), text, font=font(size, bold))
    x = box[0] + (box[2] - box[0] - bounds[2]) / 2
    y = box[1] + (box[3] - box[1] - bounds[3]) / 2 - bounds[1]
    draw.text((x, y), text, font=font(size, bold), fill=fill)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str, label: str, subtitle: str = "") -> None:
    draw.rounded_rectangle(box, radius=22, fill=fill, outline=outline, width=4)
    centered(draw, (box[0], box[1] + 55, box[2], box[3] - 36), label, 25, bold=True)
    if subtitle:
        centered(draw, (box[0], box[3] - 42, box[2], box[3] - 12), subtitle, 17, fill=MUTED)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], label: str = "") -> None:
    draw.line((*start, *end), fill=LINE, width=6)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    left = (end[0] - 18 * ux + 10 * uy, end[1] - 18 * uy - 10 * ux)
    right = (end[0] - 18 * ux - 10 * uy, end[1] - 18 * uy + 10 * ux)
    draw.polygon([end, left, right], fill=LINE)
    if label:
        centered(draw, (start[0], start[1] - 44, end[0], start[1] - 8), label, 16, fill=MUTED)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((40, 35, WIDTH - 40, HEIGHT - 35), radius=26, fill="white", outline="#D6E0EC", width=3)
    centered(draw, (40, 52, WIDTH - 40, 105), "AWS public web service architecture", 36, bold=True)
    centered(draw, (40, 105, WIDTH - 40, 140), "Design reference only — not live AWS deployment evidence", 20, fill=MUTED)

    rounded(draw, (75, 265, 260, 455), BLUE, "#2F6FA9", "External user")
    rounded(draw, (300, 265, 500, 455), GREEN, "#4E845A", "Internet Gateway", "IGW")
    arrow(draw, (260, 360), (300, 360), "HTTP")

    draw.rounded_rectangle((550, 175, 1515, 700), radius=25, fill=VPC, outline="#7C8FA6", width=4)
    centered(draw, (575, 190, 1490, 240), "VPC 10.0.0.0/16", 27, bold=True)
    arrow(draw, (500, 360), (640, 360), "0.0.0.0/0 → IGW")

    rounded(draw, (625, 265, 875, 420), GOLD, "#B87913", "Route table", "Public route")
    centered(draw, (645, 345, 855, 392), "0.0.0.0/0 → IGW", 17, bold=True, fill="#80530B")
    arrow(draw, (750, 420), (750, 485))

    draw.rounded_rectangle((590, 470, 1475, 655), radius=20, fill="#F5F8FB", outline="#A8B8C9", width=3)
    centered(draw, (610, 480, 1455, 518), "Public subnet 10.0.1.0/24", 22, bold=True)
    rounded(draw, (625, 525, 875, 625), ROSE, "#B34061", "Security group", "80: 0.0.0.0/0 | 22: learner CIDR")
    rounded(draw, (965, 525, 1195, 625), BLUE, "#5875AE", "EC2", "t3.micro")
    draw.rounded_rectangle((1275, 542, 1435, 608), radius=24, fill=INK)
    centered(draw, (1275, 542, 1435, 608), "Nginx", 23, bold=True, fill="white")
    arrow(draw, (875, 575), (965, 575), "TCP 80")
    arrow(draw, (1195, 575), (1275, 575), "HTTP")

    centered(draw, (70, 725, WIDTH - 70, 770), "Inbound request flow: External user → IGW → route table → public subnet → SG → EC2 → Nginx", 19, fill=MUTED)
    target = Path(__file__).parents[1] / "docs" / "architecture.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
