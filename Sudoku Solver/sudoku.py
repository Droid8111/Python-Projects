import os
import subprocess
from PIL import Image
import pytesseract
import cv2
import keyboard  
import subprocess
import time

# Example to check connected devices
def adb_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    print(result.stdout)


def open_app(package_name):
    command = f"adb shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    print(result.stdout)  # This will print the output of the command

def click_at_coordinates(x, y):
    # Simulate a tap at the given coordinates (x, y)
    command = f"adb shell input tap {x} {y}"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    # print(f"Tapping at coordinates: ({x}, {y})")
    # print(result.stdout)

def click_at_numbers(number):
    # Define the coordinates for each number 
    coordinates = {
        1: (90, 2400),
        2: (225, 2400),
        3: (360, 2400),
        4: (490, 2400),
        5: (626, 2400),
        6: (760, 2400),
        7: (890, 2400),
        8: (1025, 2400),
        9: (1175, 2400)
    }

    if number in coordinates:
        x, y = coordinates[number]
    else:
        print(f"Invalid number: {number}")
        return

    click_at_coordinates(x, y)
    
def click_cells(a):
    cell_size=(132, 133)
    offset=(110, 530)
    for i in range(M):
        for j in range(M):
            #time.sleep(0.25)
            click_at_numbers(a[i][j])
            x = offset[0] + j * cell_size[0] 
            y = offset[1] + i * cell_size[1]
            #time.sleep(0.25)
            click_at_coordinates(x, y)
        

# Define the location of your image
location = "c:\\Users\\ahmed\\Videos\\Sudoku pics\\Screenshot_20250104_004338.png"

# Define path to tesseract.exe (adjust to your installation path)
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

# Sudoku Solver Functions
M = 9

def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j], end=" ")
        print()

def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
    for x in range(9):
        if grid[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True

def Sudoku(grid, row, col):
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Sudoku(grid, row, col + 1)
    for num in range(1, M + 1, 1): 
        if solve(grid, row, col, num):
            grid[row][col] = num
            if Sudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

# OCR and Image Processing Functions
def preprocess_image(image_path):
    """
    Preprocesses the Sudoku image to remove grid lines and prepare it for OCR.
    """
    # Load the image in grayscale
    img = cv2.imread(image_path)
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Optional: Apply histogram equalization to improve contrast
    gry = cv2.equalizeHist(gry)

    # Detect lines and remove them
    #detector = cv2.ximgproc.createFastLineDetector(15)  # Pass length threshold as positional argument
    #lns = detector.detect(gry)
    #if lns is not None:
    #    for ln in lns:
    #        (x_start, y_start, x_end, y_end) = map(int, ln[0])  # Convert to integers
    #        cv2.line(gry, (x_start, y_start), (x_end, y_end), (255, 255, 255), thickness=2)
    
    # Apply adaptive thresholding (try adjusting kernel size and constant here)
    thr = cv2.adaptiveThreshold(gry, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 23)
    
    # Save the processed image for debugging
    #cv2.imwrite("processed_image", thr)
    return thr


def extract_grid_from_image(processed_image, cell_size=(132, 133), offset=(45, 511)):  #470 for normal 511 for battle
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            x_start = offset[0] + j * cell_size[0] +5
            y_start = offset[1] + i * cell_size[1] +10
            x_end = x_start + cell_size[0] #-5
            y_end = y_start + cell_size[1] -10
            
            cell = processed_image[y_start:y_end, x_start:x_end]
            cell_resized = cv2.resize(cell, (cell.shape[1] * 2, cell.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
            
            # Perform OCR on the cell
            cell_text = pytesseract.image_to_string(
                cell_resized , config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789"
            ).strip()

            #Handle expected errors
            if cell_text == "45":
                cell_text = "5"
            
            # Handle empty cells
            digit = int(cell_text) if cell_text.isdigit() else 0
            row.append(digit)
        grid.append(row)
    return grid

def screenshot():
    # Take a screenshot using ADB
    result = subprocess.run(["adb", "shell", "screencap", "/sdcard/screenshot.png"])
    if result.returncode != 0:
        print("Failed to take screenshot")
        return None
    
    # Pull the screenshot to the local machine
    result = subprocess.run(["adb", "pull", "/sdcard/screenshot.png", "."])
    if result.returncode != 0:
        print("Failed to pull screenshot")
        return None
    
    return "screenshot.png"

def gift():
    click_at_coordinates(650, 1200)
    time.sleep(4)
    click_at_coordinates(650, 1750)
    time.sleep(8)
    click_at_coordinates(1170, 100)
# Main Workflow
if __name__ == "__main__":

    while True:
        if keyboard.is_pressed('s'):  # Runs the whole program
            processed_image = preprocess_image(screenshot())
            cv2.imwrite("processed_sudoku.png", processed_image)
            
            # Extract the grid from the image
            sudoku_grid = extract_grid_from_image(processed_image,offset=(45, 511)) #470 for normal, 511 for battle
            print("Extracted Sudoku Grid:")
            puzzle(sudoku_grid)
            # Solve the Sudoku puzzle
            if Sudoku(sudoku_grid, 0, 0):
                print("\nSolved Sudoku Grid:")
                puzzle(sudoku_grid)
                #adb_devices()
                #open_app('easy.sudoku.puzzle.solver.free')  # This will open Sudoku app

                click_cells(sudoku_grid)
            else:
                print("Solution does not exist :(")
                break
        
        if keyboard.is_pressed('g'): # Runs the gift function
            gift()

        if keyboard.is_pressed('l'):  # End the program
            break
        #time.sleep(0.1)  # Add a small delay to avoid high CPU usage
