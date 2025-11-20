# NSI – Flappy Turtle

A playful Flappy Bird variant for the NSI project where a determined turtle swims
through an underwater landscape, dodging floating plastic waste. Procedurally
created pixel-art assets are generated at run time if they are missing, so no
binary images need to be stored in the repository.

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
created into the `assets/` directory on demand:
- `background.png` – deep-sea gradient with bubbles
- `ground.png` – sandy ocean floor
- `turtle.png` – the swimming hero
- `plastic.png` – plastic bottle obstacles (flipped vertically for top obstacles)

If you want to regenerate the images, run:
```bash
python generate_assets.py
```
The generator writes files relative to this repository. Generated images are
ignored by Git so your working tree stays clean.
