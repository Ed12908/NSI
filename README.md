# NSI – Flappy Turtle

A playful Flappy Bird variant for the NSI project where a determined turtle swims
through an underwater landscape, dodging floating plastic waste. Procedurally
created pixel-art assets are provided so the game runs out of the box.

## Requirements
- Python 3.10+
- [pygame](https://www.pygame.org/) (install with `pip install pygame`)

## Running the game
```bash
python turtle_flappy.py
```
Press **SPACE** to start swimming, flap upward, and retry after a collision.
Press **ESC** or close the window to exit.

## Assets
All images are AI-inspired procedural art generated via `generate_assets.py` and
stored in the `assets/` directory:
- `background.png` – deep-sea gradient with bubbles
- `ground.png` – sandy ocean floor
- `turtle.png` – the swimming hero
- `plastic.png` – plastic bottle obstacles (flipped vertically for top obstacles)

If you want to regenerate the images, run:
```bash
python generate_assets.py
```
