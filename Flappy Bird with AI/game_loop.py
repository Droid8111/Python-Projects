import pygame
import sys
import os
import random
import numpy as np
from bird import Bird
from pillars import Pillar
from ga import BirdAI, next_generation
from neural_network import NeuralNetwork

# Screen constants
WIDTH, HEIGHT = 800, 600
FPS_DEFAULT = 60
DIST_BETWEEN = 300

# Persistence functions

def get_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def save_fitness_data(generation, best_fitness, global_best):
    with open("fitness_data.txt", "a") as f:
        f.write(f"{generation},{best_fitness},{global_best}\n")

def save_best_bird(champion):
    if champion:
        np.savez("best_bird.npz",
                 w1=champion.brain.weights_input_hidden,
                 b1=champion.brain.bias_hidden,
                 w2=champion.brain.weights_hidden_output,
                 b2=champion.brain.bias_output)
        print("Best bird saved!")

def load_best_bird():
    try:
        data = np.load("best_bird.npz")
        brain = NeuralNetwork(7, 10, 1)  # Adjust sizes based on your neural network
        brain.weights_input_hidden = data["w1"]
        brain.bias_hidden = data["b1"]
        brain.weights_hidden_output = data["w2"]
        brain.bias_output = data["b2"]


        return brain
    except FileNotFoundError:
        print("No saved AI found!")
        return None
    except Exception as e:
        print(f"Error loading AI bird: {e}")
        return None

# Reset pillars
def reset_pillars():
    mgr = Pillar(WIDTH, HEIGHT, gap_size=150, pillar_width=80, pillar_color=(0,255,0), speed=5)
    mgr.spawn_pillar()
    return mgr, 0

# Button drawing function
def draw_button(screen, text, x, y, width, height, button_color, text_color, font):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)  # Optional: Add a border
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

# Main game loop

def run_game(train_mode: bool = False, load_ai_mode: bool = False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")

    font_big = pygame.font.Font(None, 74)
    font = pygame.font.Font(None, 36)

    # Initialize shared variables
    score = 0
    game_over = False

    # Initialize human-mode entities and stats
    if not train_mode and not load_ai_mode:
        bird = Bird(WIDTH // 6, HEIGHT // 2)
        high_score = get_high_score()  # Load high score for human mode

    # Initialize AI-mode entities and stats
    if train_mode:
        pop_size = 50
        mutation_rate = 0.1
        generation = 1
        birds = [BirdAI(WIDTH // 6, HEIGHT // 2) for _ in range(pop_size)]
        old_birds = []
        global_champion = None
        current_gen_high = 0
        train_high = 0
        # Slider UI
        slider_x, slider_y = 250, HEIGHT - 50
        slider_w, slider_h = 400, 10
        knob_r = 10
        slider_min, slider_max = 1, 1000
        fps = FPS_DEFAULT
        knob_x = slider_x + (fps - slider_min) / (slider_max - slider_min) * slider_w

    # Initialize AI solo mode
    if load_ai_mode:
        brain = load_best_bird()
        if brain is None:
            pygame.quit()
            sys.exit()
        bird = Bird(WIDTH // 6, HEIGHT // 2)
        bird.brain = brain  # Assign the loaded brain to the bird
        high_score = get_high_score()  # Load high score for AI solo mode

    # Shared pillar manager
    pillar_mgr, distance_counter = reset_pillars()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            # Human jump
            if e.type == pygame.KEYDOWN and not train_mode and not load_ai_mode and not game_over and e.key == pygame.K_SPACE:
                bird.jump()

            # Play again on space key press
            if e.type == pygame.KEYDOWN and game_over and e.key == pygame.K_SPACE:
                # Reset game state
                score = 0
                game_over = False
                bird = Bird(WIDTH // 6, HEIGHT // 2)
                pillar_mgr, distance_counter = reset_pillars()
                return run_game(train_mode, load_ai_mode)
            # Mouse controls
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos() 

                if game_over:

                    # Check Play Again button first
                    if play_again_btn.collidepoint(e.pos): 
                        # Reset game state
                        score = 0
                        game_over = False
                        bird = Bird(WIDTH // 6, HEIGHT // 2)
                        pillar_mgr, distance_counter = reset_pillars()
                        return run_game(train_mode, load_ai_mode)  # Restart the game

                    # Check Main Menu button second
                    elif main_menu_btn.collidepoint(e.pos): 

                        return  # Exit the game loop to return to the main menu

                if train_mode:
                    # Drag slider
                    if slider_x <= mx <= slider_x + slider_w and slider_y - knob_r <= my <= slider_y + knob_r:
                        knob_x = mx
                        fps = int(slider_min + (knob_x - slider_x) / slider_w * (slider_max - slider_min))
                    # Save champion
                    save_btn = pygame.Rect(10, HEIGHT - 60, 180, 40)
                    if save_btn.collidepoint(mx, my):
                        save_best_bird(global_champion)
                    # Main Menu button
                    main_menu_btn = pygame.Rect(10, HEIGHT - 110, 180, 40)
                    if main_menu_btn.collidepoint(mx, my):
                        return
                    
                if load_ai_mode:
                    # Main Menu button
                    main_menu_btn = pygame.Rect(10, HEIGHT - 110, 180, 40)
                    if main_menu_btn.collidepoint(mx, my):
                        return
                    
        # Update game state
        if not game_over:
            # Pillar spawning
            distance_counter += pillar_mgr.speed
            if distance_counter >= DIST_BETWEEN:
                pillar_mgr.spawn_pillar()
                distance_counter = 0

            # AI solo mode update
            if load_ai_mode:
                bird.update()
                rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2)

                # AI decision-making
                next_pillar = None
                for tp, bp, _ in pillar_mgr.pillars:
                    if tp.x + tp.width > bird.x:
                        next_pillar = (tp, bp)
                        break
                if next_pillar:
                    top, bottom = next_pillar
                    gap_center = top.height + (bottom.y - top.height) / 2

                    # Use second pillar if available
                    if len(pillar_mgr.pillars) > 1:
                        next_next_pillar = pillar_mgr.pillars[1]
                        top2, bottom2, _ = next_next_pillar
                        gap_center2 = top2.height + (bottom2.y - top2.height) / 2
                        x2_relative = (top2.x - bird.x) / WIDTH
                        gap2_relative = (gap_center2 - bird.y) / HEIGHT
                    else:
                        x2_relative = 1.0
                        gap2_relative = 0.0

                    inputs = np.array([
                        bird.y / HEIGHT,
                        np.tanh(bird.velocity / 20),
                        (top.x - bird.x) / WIDTH,
                        (gap_center - bird.y) / HEIGHT,
                        (bird.velocity - (gap_center - bird.y)) / 200,
                        x2_relative,
                        gap2_relative
                    ])

                    output = bird.brain.forward(inputs)

                    if output[0] > 0.5:
                        bird.jump()

                # Collision detection
                for idx, (tp, bp, sc) in enumerate(pillar_mgr.pillars):
                    if rect.colliderect(tp) or rect.colliderect(bp):
                        game_over = True
                    if not sc and bird.x > tp.x + tp.width:
                        score += 1
                        pillar_mgr.pillars[idx] = (tp, bp, True)
                if bird.y < 0 or bird.y + bird.radius > HEIGHT:
                    game_over = True

            # Training mode update
            elif train_mode:
                for b in birds[:]:
                    b.update()
                    b.fitness += 1
                    # Find next two pillars
                    next_p, next2 = None, None
                    for i, p in enumerate(pillar_mgr.pillars):
                        if p[0].x + p[0].width > b.x:
                            next_p = p
                            if i + 1 < len(pillar_mgr.pillars):
                                next2 = pillar_mgr.pillars[i + 1]
                            break
                    if next_p:
                        b.think(next_p, next2)
                    # Collision detection
                    rect = pygame.Rect(b.x - b.radius, b.y - b.radius, b.radius * 2, b.radius * 2)
                    dead = (b.y < 0 or b.y > HEIGHT or
                            any(rect.colliderect(tp) or rect.colliderect(bp) for tp, bp, _ in pillar_mgr.pillars))
                    if dead:
                        b.fitness += score
                        old_birds.append(b)
                        birds.remove(b)
                    else:
                        if b.fitness > current_gen_high:
                            current_gen_high = b.fitness
                            if current_gen_high > train_high:
                                train_high = current_gen_high
                # End of generation
                if not birds:
                    old_birds.sort(key=lambda x: x.fitness, reverse=True)
                    best_f = old_birds[0].fitness

                    # Update global champion
                    if not global_champion or best_f > global_champion.fitness:
                        global_champion = old_birds[0]
                        print(f"New global champion found with fitness: {global_champion.fitness}")


                    # Generate the next generation
                    birds, global_champion = next_generation(
                        old_birds, mutation_rate, WIDTH // 6, HEIGHT // 2, global_champion
                    )
                    old_birds.clear()
                    generation += 1
                    current_gen_high = 0
                    pillar_mgr, distance_counter = reset_pillars()

            # Human mode update
            else:
                if not hasattr(bird, 'has_jumped'):
                    bird.jump()
                    bird.has_jumped = True
                bird.update()
                rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2)
                for idx, (tp, bp, sc) in enumerate(pillar_mgr.pillars):
                    if rect.colliderect(tp) or rect.colliderect(bp):
                        game_over = True
                    if not sc and bird.x > tp.x + tp.width:
                        score += 1
                        pillar_mgr.pillars[idx] = (tp, bp, True)
                if bird.y < 0 or bird.y + bird.radius > HEIGHT:
                    game_over = True

                # Update high score on game over
                if game_over:
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)

        # Move pillars only if the game is not over
        if not game_over:
            pillar_mgr.update_pillars()

        # Rendering
        screen.fill((113, 136, 230))

        # Draw pillars first
        pillar_mgr.draw_pillars(screen)

        if train_mode:
            # Render training mode stats
            for b in birds:
                pygame.draw.circle(screen, (255, 255, 0), (b.x, int(b.y)), b.radius)
            screen.blit(font.render(f"Gen: {generation}", True, (255, 255, 255)), (10, 10))
            screen.blit(font.render(f"GenHigh: {current_gen_high}", True, (255, 255, 255)), (10, 50))
            screen.blit(font.render(f"AllHigh: {train_high}", True, (255, 255, 255)), (10, 90))

            # Render slider
            pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_w, slider_h))
            pygame.draw.circle(screen, (255, 0, 0), (int(knob_x), slider_y + slider_h // 2), knob_r)
            screen.blit(font.render(f"FPS: {fps}", True, (255, 255, 255)), (slider_x + slider_w + 10, slider_y - 10))

            # Render save button
            save_btn = pygame.Rect(10, HEIGHT - 60, 180, 40)
            pygame.draw.rect(screen, (0, 255, 0), save_btn)
            screen.blit(font.render("Save Best Bird", True, (255, 255, 255)), (15, HEIGHT - 53))

            # Render Main Menu button
            main_menu_btn = pygame.Rect(10, HEIGHT - 110, 180, 40)
            pygame.draw.rect(screen, (255, 0, 0), main_menu_btn)
            screen.blit(font.render("Main Menu", True, (255, 255, 255)), (35, HEIGHT - 103))

        elif load_ai_mode:
            # Render AI solo mode
            bird.draw(screen)
            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
            screen.blit(font.render(f"High: {high_score}", True, (255, 255, 255)), (10, 50))

            # Render Main Menu button   
            main_menu_btn = pygame.Rect(10, HEIGHT - 110, 180, 40)
            pygame.draw.rect(screen, (255, 0, 0), main_menu_btn)
            screen.blit(font.render("Main Menu", True, (255, 255, 255)), (35, HEIGHT - 103))

        else:
            # Render human mode
            bird.draw(screen)
            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
            screen.blit(font.render(f"High: {high_score}", True, (255, 255, 255)), (10, 50))

        if game_over: 

            # Render "Game Over" text
            game_over_text = font_big.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 120))

            # Draw buttons
            play_again_btn = draw_button(
                screen, "Play Again", WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 50, (0, 150, 255), (255, 255, 255), font
            )
            main_menu_btn = draw_button(
                screen, "Main Menu", WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50, (0, 150, 255), (255, 255, 255), font
            )

            pygame.display.flip()

            # Handle button clicks
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN: 

                    # Check Play Again button first
                    if play_again_btn.collidepoint(e.pos): 
                        # Reset game state
                        score = 0
                        game_over = False
                        bird = Bird(WIDTH // 6, HEIGHT // 2)
                        pillar_mgr, distance_counter = reset_pillars()
                        return run_game(train_mode, load_ai_mode)  # Restart the game

                    # Check Main Menu button second
                    elif main_menu_btn.collidepoint(e.pos): 
                        return  # Exit the game loop to return to the main menu

        pygame.display.flip()
        clock.tick(fps if train_mode else FPS_DEFAULT)

    pygame.quit()
    sys.exit()

