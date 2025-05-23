import pygame
import sys
from human_mode import run_human_mode
from ai_mode import run_training_mode
from ai_mode import run_ai_mode

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def draw_button(text, y):
    btn_rect = pygame.Rect(WIDTH // 2 - 100, y, 200, 50)
    pygame.draw.rect(screen, (0, 150, 255), btn_rect)
    text_surf = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

def main_menu():
    while True:
        screen.fill((30, 30, 30))  # Clear the screen
        title = font.render("Flappy Bird", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Draw buttons
        play_button = draw_button("Play", 250)
        train_button = draw_button("Train", 350)
        load_ai_button = draw_button("Load AI", 450)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(e.pos):
                    return "play"  # Return a signal to start the game
                if train_button.collidepoint(e.pos):
                    return "train"  # Return a signal to start training mode
                if load_ai_button.collidepoint(e.pos):
                    return "load_ai"  # Return a signal to start AI mode

        clock.tick(60)

if __name__ == "__main__":
    while True:
        mode = main_menu()  # Get the selected mode from the main menu
        if mode == "play":
            run_human_mode()  # Start human mode
        elif mode == "train":
            run_training_mode()  # Start training mode
        elif mode == "load_ai":
            run_ai_mode()  # Start AI mode