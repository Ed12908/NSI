"""Underwater Flappy Turtle game.

Run with:
    python turtle_flappy.py

The game uses pygame to recreate a Flappy Bird style experience where a turtle
swims through floating plastic waste. Assets are generated procedurally and
created automatically if missing.
"""

import os
import random
import sys
from pathlib import Path

import pygame
import generate_assets

# Screen configuration
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
GROUND_HEIGHT = 120
FPS = 60

# Gameplay tuning
# Gameplay tuning
GRAVITY = 0.35
FLAP_STRENGTH = -8.5
OBSTACLE_GAP = 190
OBSTACLE_INTERVAL = 1500  # milliseconds
SCROLL_SPEED = 3
ASSET_FILES = [
    "background.png",
    "ground.png",
    "turtle.png",
    "plastic.png",
]


def ensure_assets(asset_dir: Path):
    missing = [name for name in ASSET_FILES if not (asset_dir / name).exists()]
    if missing:
        print(f"Generating assets because missing: {', '.join(missing)}")
        generate_assets.main(asset_dir)


class UnderwaterRunner:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Turtle")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 32)
        self.large_font = pygame.font.SysFont("arial", 46, bold=True)

        self.asset_dir = Path(__file__).parent / "assets"
        ensure_assets(self.asset_dir)
        self.background = self.load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ground_img = self.load_image("ground.png")
        self.ground_width = self.ground_img.get_width()
        self.ground_offset = 0

        self.turtle_img = self.load_image("turtle.png")
        self.plastic_img = self.load_image("plastic.png")
        self.top_plastic_img = pygame.transform.flip(self.plastic_img, False, True)

        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, OBSTACLE_INTERVAL)

        self.reset()

    def load_image(self, name: str, scale_to=None):
        path = self.asset_dir / name
        image = pygame.image.load(path).convert_alpha()
        if scale_to:
            image = pygame.transform.smoothscale(image, scale_to)
        return image

    def reset(self):
        self.turtle_rect = self.turtle_img.get_rect()
        self.turtle_rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.turtle_vel = 0
        self.obstacles = []
        self.score = 0
        self.state = "start"  # start, playing, gameover

    def spawn_obstacle(self):
        margin = 80
        max_top = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_GAP - margin
        gap_y = random.randint(120, max_top)
        x = SCREEN_WIDTH + 50
        self.obstacles.append({"x": x, "gap_y": gap_y, "passed": False})

    def apply_physics(self):
        self.turtle_vel += GRAVITY
        self.turtle_rect.centery += int(self.turtle_vel)

    def flap(self):
        self.turtle_vel = FLAP_STRENGTH

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle["x"] -= SCROLL_SPEED
        self.obstacles = [o for o in self.obstacles if o["x"] > -self.plastic_img.get_width() * 2]

    def check_collisions(self):
        # Ground and ceiling
        if self.turtle_rect.top <= 0:
            return True
        if self.turtle_rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT + 5:
            return True

        turtle_mask = pygame.mask.from_surface(self.turtle_img)
        for obstacle in self.obstacles:
            x = obstacle["x"]
            gap_y = obstacle["gap_y"]
            top_rect = self.top_plastic_img.get_rect(midbottom=(x, gap_y - OBSTACLE_GAP // 2))
            bottom_rect = self.plastic_img.get_rect(midtop=(x, gap_y + OBSTACLE_GAP // 2))

            if self._mask_overlap(turtle_mask, self.turtle_rect, self.top_plastic_img, top_rect):
                return True
            if self._mask_overlap(turtle_mask, self.turtle_rect, self.plastic_img, bottom_rect):
                return True
        return False

    def _mask_overlap(self, turtle_mask, turtle_rect, other_surface, other_rect):
        offset = (other_rect.left - turtle_rect.left, other_rect.top - turtle_rect.top)
        other_mask = pygame.mask.from_surface(other_surface)
        return turtle_mask.overlap(other_mask, offset) is not None

    def update_score(self):
        for obstacle in self.obstacles:
            if not obstacle["passed"] and obstacle["x"] + self.plastic_img.get_width() // 2 < self.turtle_rect.centerx:
                obstacle["passed"] = True
                self.score += 1

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            x = obstacle["x"]
            gap_y = obstacle["gap_y"]
            top_rect = self.top_plastic_img.get_rect(midbottom=(x, gap_y - OBSTACLE_GAP // 2))
            bottom_rect = self.plastic_img.get_rect(midtop=(x, gap_y + OBSTACLE_GAP // 2))
            self.screen.blit(self.top_plastic_img, top_rect)
            self.screen.blit(self.plastic_img, bottom_rect)

    def draw_turtle(self):
        angle = max(-25, min(25, -self.turtle_vel * 2))
        rotated = pygame.transform.rotate(self.turtle_img, angle)
        rect = rotated.get_rect(center=self.turtle_rect.center)
        self.screen.blit(rotated, rect)

    def draw_ground(self):
        self.ground_offset = (self.ground_offset - SCROLL_SPEED) % self.ground_width
        x = -self.ground_offset
        while x < SCREEN_WIDTH:
            self.screen.blit(self.ground_img, (x, SCREEN_HEIGHT - self.ground_img.get_height()))
            x += self.ground_width

    def draw_text_center(self, text, y, large=False):
        font = self.large_font if large else self.font
        surface = font.render(text, True, (240, 250, 255))
        rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        outline = pygame.Surface((rect.width + 6, rect.height + 6), pygame.SRCALPHA)
        outline.fill((0, 0, 0, 80))
        outline_rect = outline.get_rect(center=rect.center)
        self.screen.blit(outline, outline_rect)
        self.screen.blit(surface, rect)

    def render(self):
        self.draw_background()
        self.draw_obstacles()
        self.draw_turtle()
        self.draw_ground()
        self.draw_text_center(f"Score: {self.score}", 40)

        if self.state == "start":
            self.draw_text_center("Flappy Turtle", SCREEN_HEIGHT // 2 - 60, large=True)
            self.draw_text_center("Press SPACE to swim", SCREEN_HEIGHT // 2)
        elif self.state == "gameover":
            self.draw_text_center("Plastic got you!", SCREEN_HEIGHT // 2 - 40, large=True)
            self.draw_text_center("Press SPACE to try again", SCREEN_HEIGHT // 2 + 10)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if self.state == "start":
                            self.state = "playing"
                            self.flap()
                        elif self.state == "playing":
                            self.flap()
                        elif self.state == "gameover":
                            self.reset()
                elif event.type == self.spawn_event and self.state == "playing":
                    self.spawn_obstacle()

            if self.state == "playing":
                self.apply_physics()
                self.move_obstacles()
                self.update_score()
                if self.check_collisions():
                    self.state = "gameover"

            self.render()

        pygame.quit()
        sys.exit()


def main():
    # Ensure assets are available even if launched from another directory
    os.chdir(Path(__file__).parent)
    game = UnderwaterRunner()
    game.run()


if __name__ == "__main__":
    main()
