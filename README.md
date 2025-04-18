# Python Game Development Exploration

This repository serves as a playground for exploring and testing various Python game development capabilities. It aims to demonstrate different approaches, libraries, and techniques for creating games in Python.

## Games

### 1. Catch the Star (Pygame)

A fun arcade-style game where you control a frog trying to catch falling stars while avoiding obstacles. [Go to game directory](catch_the_star/) (More info and screenshots)

![Gameplay](catch_the_star/docs/images/catch_the_star_gameplay.png) 

**Game Description:**
Control a character (yes, this is a frog!) to catch falling stars of different colors:
- 🌟 Yellow stars give you 1 point
- 💚 Green stars give you 3 points and restore 1 heart
- ❌ Red stars end your game on contact

Miss a green star and you'll lose a heart (and 2 points). Lose all hearts and it's game over!

The game gets progressively harder as your score increases, with stars falling faster (speed increases every 10 points).

**Features:**
- Multiple game screens (Home, Instructions, Game, Game Over)
- Progressive difficulty with increasing speed
- Heart system for multiple lives
- Score tracking (current, high score, and last score)

**Technical Details:**
- Built with Pygame 2.6.1
- Python 3.12.8
- Custom shape rendering for all game objects
- Smooth animations and collision detection
- State management for different game screens

**How to Run:**
```bash
# Make sure you have Python and Pygame installed
pip install pygame

# Navigate to the game directory
cd catch_the_star

# Run the game
python catch_the_star.py
```

### 2. Snake Game (Pygame)

A classic Snake game implementation where you control a snake that grows as it eats food. [Go to game directory](snake_game/) | [Detailed instructions](snake_game/README.md)

![Gameplay](snake_game/docs/images/snake_game_gameplay.png)

**Game Description:**
In this classic game, you control a snake that grows longer as it eats food. The goal is to eat as much food as possible without running into yourself.

**Features:**
- Simple and intuitive controls with arrow keys
- Power-ups that provide bonus points
- Screen wrapping (go through walls to come out the other side)
- High score tracking

**Game Elements:**
- **Snake**: The green character you control
- **Red apples**: Regular food that gives 1 point and makes your snake grow
- **Yellow power-ups**: Special items that give 5 bonus points

**How to Run:**
```bash
# Make sure you have Python and Pygame installed
pip install pygame

# Navigate to the game directory
cd snake_game

# Run the game
python snake_game.py
```

## Project Structure
```
.
├── README.md
├── catch_the_star/
│   ├── catch_the_star.py
│   ├── README.md
│   └── docs/
│       └── images/           # Game screenshots
└── snake_game/
    ├── snake_game.py
    ├── README.md
    └── docs/
        └── images/           # Game screenshots
```
