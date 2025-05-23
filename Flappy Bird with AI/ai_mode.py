from game_loop import run_game

def run_training_mode():
    run_game(train_mode=True)

def run_ai_mode():
    run_game(train_mode=False, load_ai_mode=True)