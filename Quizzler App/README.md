This Python project is a quiz game built using the Tkinter library for the graphical user interface (GUI) and an API for fetching trivia questions. The game presents multiple-choice questions, where the user has to answer "True" or "False."

Features:
Question Fetching: The app pulls 10 true/false questions from the Open Trivia Database API.
Interactive GUI: A simple and responsive interface built using Tkinter, where the user answers questions by pressing "True" or "False" buttons.
Score Tracking: The user’s score is updated dynamically as they answer questions. After completing the quiz, the final score is displayed.
Quiz Navigation: Users can go through the quiz, one question at a time, with immediate feedback on their answers (green for correct, red for incorrect).
End of Quiz: Once all the questions are answered, a summary screen displays the user's final score.
Workflow:
The app fetches 10 true/false questions from the Open Trivia Database.
Each question is displayed with "True" and "False" buttons.
When the user answers, the app checks the correctness and updates the score.
The next question appears after each answer.
Once all questions are answered, the final score is displayed.
File Structure:
main.py: The main program file that initializes the quiz and runs the game.
quiz_brain.py: Contains the logic for managing the quiz, including fetching questions, checking answers, and tracking score.
ui.py: Contains the GUI setup for the quiz interface.
images/: Folder containing images for the True/False buttons.
Tested for functionality, ensuring smooth transitions between questions and accurate score tracking